import React, { useState } from 'react';
import './App.css';
import SchemaSelector from './components/SchemaSelector';
import FilterForm from './components/FilterForm';
import TransformationForm from './components/TransformationForm';

const App = () => {
  const [schemas, setSchemas] = useState([]);
  const [transformations, setTransformations] = useState([])
  const [selectedSchema, setSelectedSchema] = useState('');
  const [showFilterForm, setShowFilterForm] = useState(false);
  const [columns, setColumns] = useState([]);
  const [columnDetails, setColumnDetails] = useState({});
  const [query, setQuery] = useState(''); // State to hold the current query

  const fetchSchemas = () => {
    fetch('http://localhost:5011/schemas')
      .then((response) => response.json())
      .then((data) => {
        setSchemas(data.schemas);
        setSelectedSchema('');
        setShowFilterForm(false);
        setColumns([]);
        setColumnDetails({});
        setQuery(''); // Reset the query
      })
      .catch((error) => console.error('Error fetching schemas:', error));
  };

  const fetchTransformations = () => {
    fetch('http://localhost:5011/transformations')
        .then(response => response.json())
        .then(data => {
            console.log('Available Transformations:', data.transformations);
            // Optional: Save them in state if you need to access them later
            setTransformations(data.transformations);
        })
        .catch(error => {
            console.error('Error fetching transformations:', error);
        });
    };

  const handleChangeSchema = (event) => {
    const schemaName = event.target.value;
    setSelectedSchema(schemaName);

    fetch('http://localhost:5011/schema/'+schemaName, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ schema: schemaName }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === "Schema selected") {
          const columnsData = data.selected_schema; // Expecting structured data
          const columnNames = Object.keys(columnsData);
          setColumns(columnNames);
          setColumnDetails(columnsData); // Store full column details

          setShowFilterForm(true); // Show the filter form
        } else {
          console.error(data.message); // Handle error if needed.
        }
      })
      .catch(error => console.error('Error selecting schema:', error));

    fetch('http://localhost:5011/transformations', {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === "success") {
          setTransformations(data.transformations);
        } else {
          console.error(data.message); // Handle error if needed.
        }
      })
      .catch(error => console.error('Error selecting schema:', error));
  };



  const handleFilterSubmit = (filterData) => {

    // Call API to add the filter (adjust the URL and method according to your backend)
    fetch('http://localhost:5011/filter/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(filterData),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        fetchCurrentQuery(); // Now this will wait for the filter to be added successfully
      })
      .catch(error => {
        console.error('Error adding filter:', error);
      });

  };

  const handleTransformationSubmit = (filterData) => {

    // Call API to add the filter (adjust the URL and method according to your backend)
    fetch('http://localhost:5011/transformation/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(filterData),
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        fetchCurrentQuery(); // Now this will wait for the transformation to be added successfully
      })
      .catch(error => {
        console.error('Error adding filter:', error);
      });

  };

  const handleReset = () => {
    setColumns([]);
    setColumnDetails({});
    setQuery(''); // Reset the query state
    setShowFilterForm(false);
  };

    const fetchCurrentQuery = () => {
    fetch('http://localhost:5011/query')
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        setQuery(data.query); // Update the current query state with the fetched data
      })
      .catch(error => {
        console.error('Error fetching current query:', error);
      });
  };

return (
    <div className="container">
        <h1>Available Schemas</h1>
        <button onClick={fetchSchemas}>Load Schemas</button>
        {!showFilterForm ? (
            <SchemaSelector
                schemas={schemas}
                selectedSchema={selectedSchema}
                onChange={handleChangeSchema}
            />
        ) : (
            <div>
                <h2>Selected Schema: {selectedSchema}</h2>
                <FilterForm
                    columns={columns}
                    columnDetails={columnDetails}
                    onFilterSubmit={handleFilterSubmit}
                />
                <TransformationForm
                    transformations={transformations}
                    onTransformationSubmit={handleTransformationSubmit}
                  />

                <button onClick={handleReset} className="reset-btn">Reset</button>

                {/* Display the current query as a textarea */}
                <div className="query-box">
                    <h3>Current Query:</h3>
                    <textarea
                        value={query}
                        readOnly
                        rows="3"
                        style={{
                            width: '100%',
                            padding: '10px',
                            border: '1px solid #ccc',
                            borderRadius: '5px',
                            resize: 'none'
                        }}
                    />
                </div>
            </div>
        )}
    </div>
);

};

export default App;
