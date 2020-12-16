# imp_predict
Impression prediction scripts for model version 2.0

# Training details for Generation 2.0
- The Generation 2.0 code is based on a Graph Transformer neural network
- The Gen2.0 model is trained on Dataset 4: 772 small molecules from the CSD, with optimised structures and NMR parameters
calculated with DFT (add dft details, or link to paper)
- Validation was done on 442 random molecules again from the CSD

# Performance metrics
- add performance of model


# Instructions for use:
1. Download this repository
2. Obtain trained models from the butts group
3. create the following folders: INPUT, OUTPUT, MODEL
4. run the make_conda_env.sh script to create the conda environments
5. put molecule you want to process inside the INPUT folder
6. run predict.sh the output molecules should be inside OUTPUT
