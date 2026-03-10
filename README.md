# DrugLM - Medication Safety Assistant

DrugLM is a medication safety assistant project, providing an intelligent system for detecting and analyzing drug-drug interactions (DDIs). The solution leverages knowledge distillation to power a local Small Language Model (SLM), engineered to achieve near-LLM accuracy while delivering significantly faster and lower-cost inferences.

## Key Features

- **Small Language Model (SLM) Integration**: Powered by a locally hosted model trained through knowledge distillation from larger LLM responses, ensuring high accuracy on complex medical queries.
- **RAG Architecture**: Employs a Retrieval-Augmented Generation (RAG) pipeline to cross-reference natural language queries with a comprehensive, fast-retrieval drug interaction database.
- **Optimized Inference**: By shifting from external LLM APIs (like DeepSeek APIs) to a locally hosted SLM, DrugLM achieves reduced operational costs and improved response times suitable for real-time applications.
- **Drug Entity Extraction**: Automatically extracts drug names from user queries using sophisticated pattern matching and entity recognition.
- **Interaction Retrieval**: Searches backend DDI datasets to find known interactions between extracted drugs before passing context to the model.

## Example Usage
> "Can I take potassium chloride and acrivastine together? I'm also on lisinopril."

The system extracts the entities, retrieves matching DDI rows from the database, and feeds them into the SLM/LLM to output a tailored, real-time safety summary.

## Disclaimer
**This tool is for educational and research purposes only.** It is not intended to be a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of an actual physician or other qualified health provider regarding any medical condition or medication interaction queries.
