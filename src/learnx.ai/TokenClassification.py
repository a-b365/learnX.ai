from collections import OrderedDict

import torch
import evaluate
import pytorch_lightning as pl
from pytorch_lightning.loggers import MLFlowLogger
from pytorch_lightning.callbacks import Timer
from pytorch_lightning.callbacks import ModelCheckpoint
from transformers import AutoModelForTokenClassification, pipeline, AutoTokenizer


#Tags for token classification
id2label = {
    0: "I",
    1: "O",
    2: "B"
}

label2id = {
    "I": 0,
    "O": 1,
    "B": 2
}

def post_processing(text, state_dict="../../models/tc.pth"):
    
    model = AutoModelForTokenClassification.from_pretrained(
      "distilbert/distilbert-base-uncased", num_labels=3, id2label=id2label, label2id=label2id
    )

    model.load_state_dict(torch.load(state_dict))
    tokenizer = AutoTokenizer.from_pretrained("distilbert/distilbert-base-uncased")

    classifier = pipeline("ner", model=model, tokenizer=tokenizer)
    return classifier(text, aggregation_strategy="first")

def aggregate_entities(ner_output):

  entities = []
  current_entity = []

  for item in ner_output:
    if item['entity_group'] == 'B':

      if current_entity:

        entities.append(current_entity)
        current_entity = []

      current_entity.append((item['start'],item['end']))

    elif item['entity_group'] == 'I':

      current_entity.append((item['start'],item['end']))

  if current_entity:
    entities.append(current_entity)

  return entities

class TokenClassification(pl.LightningModule):
  def __init__(self, model_name_or_path, learning_rate=2e-5, **kwargs):
    super().__init__()
    self.save_hyperparameters()
    self.model = AutoModelForTokenClassification.from_pretrained(model_name_or_path, num_labels=kwargs["num_labels"], id2label=kwargs["id2label"], label2id=kwargs["label2id"])
    self.learning_rate = learning_rate
    self.seqeval = evaluate.load("seqeval")

  def forward(self,**inputs):
    return self.model(**inputs)

  def training_step(self, batch, batch_idx):
    outputs = self(**batch)
    loss = outputs[0]
    # self.train_loss.append(loss)
    self.log("train_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=False)
    return loss

#   def on_train_epoch_end(self):
#     loss = sum(self.train_loss)/len(self.train_loss)
#     self.logger.experiment.log_metric(run_id=self.logger.run_id, key="train_loss", value=loss)
#     self.train_loss.clear()

  def validation_step(self, batch, batch_idx):
    outputs = self(**batch)
    val_loss, logits = outputs[:2]
    metrics = self.compute_metrics([logits, batch["labels"]])
    # self.val_loss.append(val_loss)
    # preds = torch.argmax(logits, dim=2)
    # labels = batch["labels"]
    # self.outputs["val_loss"].append(val_loss)
    # self.outputs["preds"].append(preds)
    # self.outputs["labels"].append(labels)
    self.log_dict(metrics, on_step=False, on_epoch=True, prog_bar=True, logger=False)
    self.log("val_loss", val_loss, on_step=False, on_epoch=True, prog_bar=True, logger=False)

#   def on_validation_epoch_end(self):
#     loss = sum(self.val_loss)/len(self.val_loss)
#     self.logger.experiment.log_metric(run_id=self.logger.run_id, key="val_loss", value=loss)
#     self.val_loss.clear()

  def compute_metrics(self, p):
    predictions, labels = p
    predictions = torch.argmax(predictions, dim=2)

    true_predictions = [
        [self.hparams.id2label[p.item()] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]
    true_labels = [
        [self.hparams.id2label[l.item()] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = self.seqeval.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

  def configure_optimizers(self):
    optimizer = AdamW(model.parameters(), lr=self.hparams.learning_rate)
    # scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=self.trainer.estimated_stepping_batches)
    # scheduler = {"scheduler":scheduler, "interval":"step", "frequency":1, "monitor":"val_loss"}
    return optimizer
  
if __name__ == "__main__":
    
    checkpoint_path="../../models/last-tc.ckpt"
    model = TokenClassification.load_from_checkpoint(checkpoint_path)
    state_dict = OrderedDict()

    for i,j in model.state_dict().items():
      t = i.split(".",maxsplit=1)[1]
      i = i.replace(i,t)
      state_dict[i] = j

    torch.save(state_dict,"../../models/tc.pth")