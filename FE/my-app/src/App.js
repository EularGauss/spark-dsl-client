import React, { useState } from 'react';
import './App.css';
import SchemaSelector from './components/SchemaSelector';
import FilterForm from './components/FilterForm';

const App = () => {
  const [schemas, setSchemas] = useState([]);
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

  const handleChangeSchema = (event) => {
    const schemaName = event.target.value;
    setSelectedSchema(schemaName);

    fetch(`http://localhost:5011/schema/${schemaName}`, {
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
  };

  const handleFilterSubmit = (filterData) => {
    console.log("Submitting filter:", filterData); // Debugging log

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
        return response.json();
      })
      .then(data => {
        console.log('Filter added successfully:', data);
        // Optionally, you can update your query state here based on the response
        setQuery(data.filters.join(', ')); // Example of updating the current query
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
          <button onClick={handleReset} className="reset-btn">Reset</button>

          {/* Display the current query as a textarea */}
          <div className="query-box">
            <h3>Current Query:</h3>
            <textarea
              value={query}
              readOnly
              rows="3"
              style={{ width: '100%', padding: '10px', border: '1px solid #ccc', borderRadius: '5px', resize: 'none' }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default App;
