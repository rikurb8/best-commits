# Evals

Collection of high level evaluations for various aspects of the project. "Can I run the project with docker compose and run a playwright script browsing the store and purchasing a basket of things", "how good commit message can you produce", "code review review"

## Create commit

Goal: Create a informative but concise commit message. Focus on keeping the message informative and relevant. No absolute lenght limits but the message must be easily readable for humans.

Task: Create commit based on given diff, prompt and model

Eval: Have separate Judge evaluate commit message and rate 1-100. Show ranking of models. Judge results againts results from previous top 3

## Review unchanged commited changes

Goal: Create a Markdown formatted review of uncommited changes. No absolute lenght limits but the message must be easily readable for humans.

Task: Review unchanged files based on tests materials, evaluate result compared others in history (different model, prompt, context). Review should contain:

- Summary of changes (what, why, how large the change is, if there's anything special to take in to account)
- Correctness assessment (does it work as expected)
- Code quality assessment (does it follow best practices, are the abstractions clear and on the right level, linter passes)
- Documentation review (are all changes reflected in the documentation)
- Testing assesment (are the changes being tested, should there be other new things to tests because of the changes, tests pass)
