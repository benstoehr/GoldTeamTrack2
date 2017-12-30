# Python CSV SQL Query Tool

For Project Track 2 in CS 411, Gold Team is implementing a system that accepts SELECT-FROM-WHERE SQL queries and 
performs the query on CSV files. The CSV files may be up to 2 million rows and 300 attributes, much larger than what can
fit into a usual memory allocation. The tool creates indexes over the columns of the CSV tables of size up to 30% 
of the CSV files. Both single table queries and multi-table join queries are supported. There is a frontend
command line client that provides a REPL with query history. Additionally, there is a flask server that accepts and 
processes the queries from the client.

### Contributors

* Ben Stoehr
* Nick Tripp
* Jacob Trueb

## Quick start
### Getting the source code

Head to releases, download the latest stable build, and unzip it in your desired location.

**OR**

Navigate to your desired directory, and clone the `demo_branch` branch of this repo with

    git clone -b demo_branch git@github.com:benstoehr/GoldTeamTrack2.git

**NOTE**: From here on out, we will assume your active directory (`./`) is the root directory of the project.

### Setting a Virtual Environment (Suggested)

Both the Client and the Server require Python 3 in order to run. For a clean Python 3 setup, we suggest that you use a 
virtual environment with virtualenv. To do so, open up a bash terminal and follow the following steps:

1. Installing virtualenv: 

    If you are running Mac OSX or Linux you can probably install it with the following:
    
        sudo pip install virtualenv
        
    Otherwise, refer to[how to install virtualenv on your system](https://virtualenv.pypa.io/en/stable/installation/).

2. Create the project-specific virtual environment:

        virtualenv venv
        
3. From now on, whenever you want to activate Python 3 and the dependencies we are about to install, just run

        . venv/bin/activate
        
4. Verify that you are running Python 3:
        
        python --version
        
That's it!
   
### Installing Dependencies

Our project design makes use of several external libraries that can be easily installed whether or not you are using
a virtual environment. Just run the following:

    pip install sqlparse
    pip install Flask
    pip install python-dateutil
    pip install requests

### Running the Server

To tell Flask where our server is located, run the following:
    
    export FLASK_APP=./server/Server.py

You only need to do that once (per bash window).    
Then, run the server with the following:

    flask run

The server should now be up and running on port 5000. Be sure to leave this window open for the duration of your querying!

### Running the Client

Open up another window and navigate to the root directory of the project.

*Note that if you are using virtualenv, be sure to start it up again with* `. venv/bin/activate`
  
Then, run the client with the following:

    python client/Client.py

Everything should be running at this point.
If you see a `(Cmd)` prompt, you're good to start querying!

## Adding csv data

Copy whatever `.csv` files you want to query into the `./data`.  Each `.csv` file should contain a single table. We have provided a few files in this directory already 
for you as a sample.

## Client Command Line Tool

Our Client features REPL style input and output, accepting queries and sending them to the backend server. 
The command line tool uses builtin python modules in order to support command history and server http requests.

Commands:
* `list` - view the list of tables available to query.
* `query <SQL SELECT-FROM-WHERE Query>` - query the tables.

#### Query Structure Restrictions:

* Any quotes must be double quotes (" "), not single quotes (' ')
* All filepaths should be just the name of the file: `./data/review1m.csv` should be referred to as `review1m`.
* CSV filenames cannot contain `-`, so rename the files if they do.
* If conditionally joining tables, the conditions must be in parentheses: i.e. `ON (<conditions>)`

### Example Queries:
#### Here are what some Valid Queries would look like...

1. 
        (Cmd) query SELECT DISTINCT * FROM movies
2. 
        (Cmd) query SELECT M.title_name FROM movies M WHERE M.title_year = 2009
3. 
        (Cmd) query SELECT B.name, B.postal_code, R.review_id, R.stars, R.useful FROM business B JOIN review50k R ON (B.business_id = R.business_id) WHERE B.city = "Champaign" AND B.state = "IL"

#### ...and some Invalid Queries

1. 
        (Cmd) query "SELECT * FROM movies"    
    ***Why:*** *Don't put your SELECT query in quotes.*
2.
        (Cmd) query SELECT M.title_name FROM movies M WHERE M.movie_title = 'Avatar'
    ***Why:*** *Use double quotes, not single quotes.*
3. 
        (Cmd) query GIVE me EVERY tuple IN movies
    ***Why:*** *Invalid SQL.*
4. 
        (Cmd) query SELECT * FROM ./data/movies.csv
    ***Why:*** *Refer to filenames by just their table name. This one should be just* `movies`
5. 
        (Cmd) query SELECT * FROM business B JOIN review50k R ON B.business_id = R.business_id
    ***Why:*** *Join conditions must be in parenthesis.*
6. 
        (Cmd) query SELECT * FROM business B JOIN review-50k R ON B.business_id = R.business_id
    ***Why:*** *Tablenames must not have a*`-` *. Rename the file so that it does not have a dash.*

## A Note About Performance

The first time you run a query over a table, or a column of a table, that you hasn't accessed before, 
the system will generate index and other pre-processing files (storing them in `./data`).  This will potentially take a
long time - sometimes several minutes. **This is normal.**

Each subsequent query over that table or column of a table will be*significantly*faster, so long as those index files 
remain in the `./data` directory.

## Troubleshooting

If you experience errors, try restarting the Server and Client. Also try deleting the index and pre-processing files
(anything in the `./data` directory that doesn't end in `.csv`)

## The Server Database System

Server-side, query execution is handled by `Hangman`. The `Hangman.execute` method accepts the SQL query string. It 
calls the necessary methods to execute the query processing pipeline, wrapping each call in a timing method that prints 
to the server's stdout. The result of the query is returned in the response from flask to the client.

The query execution pipeline includes a `QueryParser` that parses the query and validates the presence of each table 
and column referenced in the query. After parsing the query with `QueryParser.parse_select_from_where`, we pass the 
tables, columns, where_conditions, and join_conditions to the `QueryOptimizer`, where we determine the order that we 
will join tables and reduce the where_conditions algebraically. The output from the `QueryOptimizer` is passed into the 
`QueryFacade` to join the tables (using pandas) and select rows according to the conditions. Conditions are checked 
according to the index for a column. We have two different types of indexes `BitmapIndex` and `BTreeIndex`. Originally, 
we only had the `BTreeIndex`, but `BitmapIndex` was added in order to support faster partial matching. Indexes are 
loaded and managed by the `TableIndexer` object, which automatically creates, loads, and saves indexes as needed by the 
`QueryFacade`.

## Libraries
* python.http.client
* python.concurrent
* python.cmd
* https://github.com/andialbrecht/sqlparse
* https://pandas.pydata.org/
* http://flask.pocoo.org/

