const bodyParser = require('body-parser')
const express = require('express')
const app = express()
const db = require('./connection')
const port = 3000

app.title = "discoapi"

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)

app.get('/filters', db.getFilters)
app.get('/filters/:freq', db.getFiltersByFreq)
app.post('/filters', db.createFilter)
app.put('/filters/:freq', db.updateFilter)
app.delete('/filters/:freq', db.deleteFilter)

app.listen(port, () => {
  console.log(`API is now listening on port ${port}`)
})
