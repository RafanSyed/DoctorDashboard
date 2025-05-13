import sys
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, Trainer, TrainingArguments

# Ensure a training CSV file path is provided on the command line
if len(sys.argv) < 2:
    print("Usage: python train_model.py <path_to_training_csv>")
    sys.exit(1)

training_csv_path = sys.argv[1]

# Load the dataset from CSV.
# The CSV file should have columns such as "transcript" and "doctor_notes"
data_files = {"train": training_csv_path, "validation": training_csv_path}  # Adjust as needed for separate files
dataset = load_dataset("csv", data_files=data_files)

# Choose a pre-trained model to fine-tune. Here, T5-small is used for prototyping.
model_name = "t5-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# Define maximum sequence lengths for inputs and outputs
max_source_length = 512
max_target_length = 128

def preprocess_function(examples):
    # Extract the input (transcript) and target (doctor_notes) texts
    inputs = examples["transcript"]
    targets = examples["doctor_notes"]
    
    # Tokenize the inputs with padding and truncation
    model_inputs = tokenizer(inputs, max_length=max_source_length, truncation=True, padding="max_length")
    
    # Tokenize the target texts; the tokenizer must be in target mode for seq2seq tasks
    with tokenizer.as_target_tokenizer():
        labels = tokenizer(targets, max_length=max_target_length, truncation=True, padding="max_length")
    
    # The labels (target token IDs) will be used by the model for computing loss
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

# Preprocess the dataset using the helper function.
tokenized_datasets = dataset.map(preprocess_function, batched=True)

# Set up the training arguments
training_args = TrainingArguments(
    output_dir="./results",            # Directory where model predictions and checkpoints will be written.
    evaluation_strategy="epoch",       # Evaluate at the end of each epoch
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=3,                # You can adjust this number based on your data size
    weight_decay=0.01,
)

# Create the Trainer object
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)

# Start the training process
trainer.train()

# Save the fine-tuned model and tokenizer for later inference
model.save_pretrained("./my-medical-model")
tokenizer.save_pretrained("./my-medical-model")
print("Training complete. Model saved in ./my-medical-model")
