from collections import OrderedDict

import torch
import numpy as np
import pytorch_lightning as pl
from transformers import T5ForConditionalGeneration, T5Tokenizer, AdamW, get_linear_schedule_with_warmup

class QAGenerator(pl.LightningModule):

  def __init__(self, model_name_or_path:str,
               learning_rate:float=2e-5,
               batch_size:int=4,
               warmup_steps:int=0,
               adam_epsilon:int=1e-8,
              ):

    super().__init__()
    self.save_hyperparameters()
    self.model = T5ForConditionalGeneration.from_pretrained(model_name_or_path)
    self.tokenizer = T5Tokenizer.from_pretrained(model_name_or_path)
    self.learning_rate = learning_rate
    # self.train_loss = []
    # self.val_loss = []

  def forward(self,**inputs):
    return self.model(input_ids=inputs["input_ids"], 
                      attention_mask=inputs["attention_mask"], 
                      decoder_attention_mask=inputs["target_mask"], 
                      labels=inputs["labels"])

  def training_step(self, batch, batch_idx):
    outputs = self(**batch)
    loss = outputs[0]
    #self.train_loss.append(loss)
    self.log("train_loss", loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
    return loss

#   def on_train_epoch_end(self):
#     loss = sum(self.train_loss)/len(self.train_loss)
#     self.logger.experiment.log_metric(run_id=self.logger.run_id, key="train_loss", value=loss)
#     self.train_loss.clear()

  def validation_step(self, batch, batch_idx):
    outputs = self(**batch)
    val_loss, logits = outputs[:2]
    predictions = torch.argmax(logits, dim=2)
    scores = self.compute_metrics([predictions, batch["labels"]])
    # self.val_loss.append(val_loss)
    # preds = torch.argmax(logits, dim=2)
    # labels = batch["labels"]
    # self.outputs["val_loss"].append(val_loss)
    # self.outputs["preds"].append(preds)
    # self.outputs["labels"].append(labels)
    self.log("val_loss", val_loss, on_step=False, on_epoch=True, prog_bar=True, logger=True)
    self.log_dict(scores, on_step=False, on_epoch=True, prog_bar=True, logger=True)


  def compute_metrics(self, eval_pred):
    predictions, labels = eval_pred
    decoded_preds = self.tokenizer.batch_decode(predictions, skip_special_tokens=True)
    labels = labels.cpu().numpy()
    labels = np.where(labels != -100, labels, self.tokenizer.pad_token_id)
    decoded_labels = self.tokenizer.batch_decode(labels, skip_special_tokens=True)
    result = rouge.compute(predictions=decoded_preds, references=decoded_labels, use_aggregator=True)
    return {k: round(v, 4) for k, v in result.items()}

#   def on_validation_epoch_end(self):
#     loss = sum(self.val_loss)/len(self.val_loss)
#     self.logger.experiment.log_metric(run_id=self.logger.run_id, key="val_loss", value=loss)
#     self.val_loss.clear()

  def configure_optimizers(self):
    optimizer = AdamW(self.model.parameters(), lr=self.hparams.learning_rate, eps=self.hparams.adam_epsilon)
    scheduler = get_linear_schedule_with_warmup(optimizer=optimizer, num_warmup_steps=self.hparams.warmup_steps, num_training_steps=self.trainer.estimated_stepping_batches)
    scheduler  = {"scheduler":scheduler, "interval":"epoch", "frequency":1, "monitor":"val_loss"}
    return [optimizer], [scheduler]
  

if __name__ == "__main__":
    
    checkpoint_path="../../models/last-t5b.ckpt"
    model = QAGenerator.load_from_checkpoint(checkpoint_path)
    state_dict = OrderedDict()

    for i,j in model.state_dict().items():
      t = i.split(".",maxsplit=1)[1]
      i = i.replace(i,t)
      state_dict[i] = j

    torch.save(state_dict,"../../models/qa-t5b.pth")