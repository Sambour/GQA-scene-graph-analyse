The GQA dataset for Real-World Visual Reasoning. Version 1.2.

All questions of the GQA dataset. Both all (unbalanced, 22M) and balanced (1.7M) versions, for 4 splits: train, val, test-dev, test and challenge.

Questions are compositional, and require a diverse set of reasoning skills. Each question comes
with an underlying semantic representation of the reasoning process needed to answer it, with visual
pointers from question words to objects within the image.

Splits:
- Train and Val: Large fully annotated (image scene graphs and all information about each question) splits for training.
- Test-Dev: A smaller split for development, annotated with answers to each of the questions. Please use it to get an estimation of the likely test scores during the development.
- Test and Challenge: Answers, annotations and other information about the images and questions is hidden. Test is used to report scores in papers, and Challenge is used for the GQA competition. 

Comments:
- For the competition we also provide an additional file called 'submission_all_questions.json' (which is the union of the questions from val, test-dev, test and challenge).
  In order to participate in the challenge, please upload your answers on all questions in that file to the GQA evaluation server: https://evalai.cloudcv.org/web/challenges/challenge-page/225/overview
- Each split has both 'balanced' and 'all' versions. The 'balanced' version contains a subset of the questions in the 'all' version, and is significantly less biased, and so it is more resilient to educated guesses based on the question alone and demands increased understanding of the image. The 'all' version is used however to measure a model's consistency across semantically similar questions. 

Versions:
- 1.0: Initial Launch.
- 1.1: Updating the questions' functional programs. Fixing some typos.
- 1.2: Introducing the Test-Dev split to get most precise estimation of likely test results during development. Update the challenge split. *All questions and images remain the same as prior versions* (only adding a new split on top of existing ones). 

Pleae visit gqadataset.org for all information about the dataset, including examples, visualizations, paper and slides.
