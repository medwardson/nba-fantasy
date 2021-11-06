const express = require('express')
const app = express()
const port = 3000

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
        password: 'LWR4_Ju85PAGkibXCj2qeKC787WX',
        port: 5432,
    });
    client.connect();

    client.query(`SELECT * FROM "medwardson/nba-data"."playerdata" 
                    WHERE player_name='${req.params.name}';`, (err, r) => {
        console.table(r.rows);
        // console.log(res.rows);
        final_data = r.rows[0];
        res.send(final_data);
    });


    // res.send(final_data);
})

app.listen(port, () => {
  console.log(`Example app listening at http://localhost:${port}`)
})