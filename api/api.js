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

app.get('/api/filters', db.getFilters)
app.get('/api/filters/:freq', db.getFiltersByFreq)
app.post('/api/filters', db.createFilter)
app.put('/api/filters/:freq', db.updateFilter)
app.delete('/api/filters/:freq', db.deleteFilter)

app.listen(port, () => {
  console.log(`API is now listening on port ${port}`)
})
