// Step 2: 
// use bookstore 
db = db.getSiblingDB("bookstore")

// Step 3: load authors.json
// paste your drop and insertMany commands here
db.authors.drop()
doc = JSON.parse(fs.readFileSync("authors.json", "utf8"))
db.authors.insertMany(doc)
// Step 4: load books.json
// paste your drop and insertMany commands here
db.books.drop()
doc = JSON.parse(fs.readFileSync("books.json", "utf8"))
db.books.insertMany(doc)
// Step 5: list authors and books
// paste your find commands here
db.authors.find()
db.books.find()
// Step 6: insert two new books
db.books.insertMany([
    {
      title: "Moneyball",
      published_year: 2003,
      author_ids: ["author_004"]
    },
    {
      title: "The Signal and the Noise",
      published_year: 2012,
      author_ids: ["author_005"]
    }
  ])
// Step 7: add missing authors
// paste your insert commands here
db.authors.insertMany([
    {
      _id: "author_004",
      name: "Michael Lewis",
      nationality: "American",
      bio: {
        short: "American author and financial journalist.",
        long: "Michael Lewis is an American writer known for nonfiction about finance, sports, and the people who challenge conventional wisdom. Before writing full time he worked as a bond salesman, which became the basis for his first book, Liar's Poker. His books include Moneyball, The Blind Side, and The Big Short, several of which have been adapted into films."
      }
    },
    {
      _id: "author_005",
      name: "Nate Silver",
      nationality: "American",
      bio: {
        short: "American statistician and election forecaster.",
        long: "Nate Silver is an American statistician and writer who first built PECOTA, a system for projecting baseball player performance. He later founded FiveThirtyEight, where his election forecasts drew national attention. His book The Signal and the Noise looks at why most predictions fail and what separates good forecasts from bad ones."
      }
    }
  ])
// Step 8: filter books by a list of authors
// paste your find command here
db.books.find({ author_ids: { $in: ["author_001", "author_004"] } })