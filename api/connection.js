const Pool = require('pg').Pool

const pool = new Pool({
    host: "localhost",
    user: "postgres",
    port: 5432,
    password: "sudisco",
    database: "disco"
})

const getFilters = (req, res) => {
  pool.query(`Select * from filters`, (err, result) => {
    if (err) {
      throw err;
    }
    res.status(200).json(result.rows);
  })
}

const getFiltersByFreq = (req, res) => {
  pool.query(`Select * from filters where freq = ${req.params.freq}`, (err, result) => {
    if (err) {
      throw err
    }
    res.status(200).json(result.rows)
  })
}

const createFilter = (req, res) => {
  const filter = req.body;
  let insertQuery = `insert into filters(freq, gain)
  values(${filter.freq}, '${filter.gain}')`

  pool.query(insertQuery, (err, result)=>{
    if (err) {
      console.log(updateQuery)
      console.log(err)
    } else {
      res.status(200).json(result.rows)
    }
  })
}

const updateFilter = (req, res) => {
  let filter = req.body;
  let updateQuery = `update filters
    set gain = '${filter.gain}'
    where id = ${filter.id}`

  pool.query(updateQuery, (err, result)=>{
    if (err) {
      console.log(updateQuery)
      console.log(err)
    } else {
      res.status(200).json(result.rows)
    }
  })
}

const deleteFilter = (req, res) => {
  let insertQuery = `delete from filters where id = ${req.params.id}`

  pool.query(insertQuery, (err, result) => {
    if (err) {
      console.log(insertQuery)
      console.log(err)
    } else {
      res.status(200).json(result.rows)
    }
  })
}

module.exports = {
  getFilters,
  getFiltersByFreq,
  createFilter,
  updateFilter,
  deleteFilter
}
