import OpenAI from 'openai';

const openai = new OpenAI({
    organizations: "org-FCymhZNKK2HGhYzF5IIFUVig",
    apiKey: "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",
});

const chatCompletion = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [
        {role: "system", content: "You are the best music recommender, based on a short prompt, \
         you are going to return number values according to tempo, valence, danceability, genre, mood, and timbre to be used with spotify's api."},
        {role: "user", content: "I am going to the gym soon, I want music that will get me excited."},
    ],
});

console.log(chatCompletion.choices[0].message);