const express = require('express');
const bodyParser = require('body-parser');


const app = express();

app.set('PORT', process.env.PORT || 3000);
app.set('MONGO_HOST', process.env.MONGO_HOST);
app.set('MONGO_DATABASE', process.env.MONGO_DATABASE);

app.use(bodyParser.json()); 
app.use(bodyParser.urlencoded({ extended: true })); 

app.get('/', (req, res) => {
    res.json({ message: 'It works!' });
});

app.post('/login', async (req, res) => {
    const db = app.get('db');
    const username = req.body.username;
    const password = req.body.password;
    const user = await db.collection('users').findOne({
        username, password
    });
    if (user) {
        res.json({ message: 'success' });
    } else {
        res.json({ message: 'fail' });
    };
});

const MongoClient = require('mongodb').MongoClient;
MongoClient.connect(app.get('MONGO_HOST'), (err, client) => {
    if (err) {
        throw err;
    }
    console.log(`Connected to database ${app.get('MONGO_HOST')}`);
    app.set('db', client.db(app.get('MONGO_DATABASE')));
    app.listen(app.get('PORT'), () => {
        console.log(`Listening on ${app.get('PORT')}`);
    });
});
