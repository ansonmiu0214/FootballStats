const sqlite3 = require('sqlite3').verbose();

function checkDatabaseConnection() {
  const db = new sqlite3.Database('./instance/footballDB.db', (err) => {
    if (err) {
      console.error('Error connecting to the database:', err.message);
      return;
    }
    console.log('Connected to the footballDB database.');
    db.close((error) => {
      if (error) {
        console.error('Error closing the database connection:', error.message);
      } else {
        console.log('Database connection closed.');
      }
    });
  });
}

