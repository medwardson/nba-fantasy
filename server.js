const express = require('express')
const app = express()
const port = 3000
if (process.env.NODE_ENV !== 'production') {
    require('dotenv').config();
}
const { Client } = require('pg');

app.get('/', (req, res) => {
    res.send("Welcome to NBA Stats");
})

app.get('/player/:name', (req, res) => {
    let final_data;
    const client = new Client({
        user: 'medwardson_demo_db_connection',
        host: 'db.bit.io',
        database: 'bitdotio',
        password: process.env.PASSWORD,
        port: 5432,
    });
    client.connect();

    client.query(`SELECT * FROM "medwardson/nba-data"."playerdata" 
                    WHERE player_name='${req.params.name}';`, (err, r) => {
        console.table(r.rows);
        final_data = r.rows[0];
        if (final_data) {
            res.send(final_data);
        } else {
            res.send("Error - No player by that name was found.")
        }
        client.end();
    });
})

app.listen(process.env.PORT || port), () => {
  console.log(`Example app listening at http://localhost:${port}`);
}