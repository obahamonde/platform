const express = require('express');

const app = express().use(express.json());


app.get('/', (req, res) => {
    res.json({ message: "Hello World" });
});

app.listen(8080, () => {
    console.log('http://localhost:8080');
});
