---
title: AI Quiz Generation with React.js 
date: 2025-01-03
time: 1:41pm
---


While in University my friend and I developed similar strategies for using AI to prepare for exams. We would prompt ChatGPT, asking it to generate a quiz to test our knowledge on a subject based on subjects and keywords that we provided. For example, a prompt we may have used is:

> “Generate an exam to test my knowledge on relational algebra. After I provide you with my answers give me feedback on whether they were correct and how they can be improved.”
> 

After we discovered that we both used AI in this way, we decided to make an application that will allow users to generate quizzes based on keywords and take them in an interactive online web application. 

### OpenAI API

We used the OpenAI API to generate the quizzes. In order to make verifying output as easy as possible we opted for making all the questions in the multiple choice style. After some experimenting here is what our prompt to the ChatGPT API ended up looking like:

<pre><code class="language-python">
You are an AI quiz generation companion. You will be given a series of subjects, and your response will be a JSON file of a ${num_questions}-question multiple choice quiz which covers the provided list of topics.\
                          The quiz must be ACCURATE AND CORRECT, and you MUST WRITE THE QUIZ IN THIS EXACT JSON FORMAT: 
                        {
                            questions: [
                                {
                                "question": "Question goes here",
                                "options": [
                                    "option 1",
                                    "option 2",
                                    "option 3",
                                    "option 4"
                                ],
                                "correct_answer": "option 2",
                                "explanation": "Explanation of the correct answer goes here"
                                }
                            ]
                        }

                        Follow the exact provided JSON format and make a quiz with ${num_questions} multiple choice questions. There should be ${num_questions} objects inside of the “questions” array that correspond to the ${num_questions} questions. 
Return ONLY THE JSON OBJECT and do not deviate.
</code></pre>

`num_questions` is a variable that is set earlier in the code that we set to 5. 

### React

We anticipated the need to dynamically generate UI components based on the data we received from the API call. We chose to use React as our framework because it solved this issue in an elegant way. We created a quiz component inside a `Quiz.jsx` file that accepted the json object from the API call and created an interactive quiz. As the user clicks answers questions they are given feedback on whether or not they answered correctly and an explanation is revealed detailing why the correct answer is correct. 

*Selecting an incorrect answer:*

<img class="responsive-img" src="/static/images/incorrect_answer_example.png" alt="Incorrect Answer Example">

*Selecting a correct answer:*

<img class="responsive-img" src="/static/images/correct_answer_example.png" alt="Correct Answer Example">

### Conclusion

This was a fun and simple app to create that allowed for the opportunity to learn about the OpenAI API and how to use React to generate and display quiz components dynamically. It would be interesting to expand this project to support short answer questions that are sent back to the LLM to be reviewed. This would require a lot more API calls and may not be worth it, but it could be a valuable learning tool for students to get direct feedback based on their written answers.