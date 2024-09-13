import React, { useState } from 'react';
import './App.css';
import SchemaSelector from './components/SchemaSelector';
import FilterFields from './components/FilterFields';

const App = () => {
  const [schemas, setSchemas] = useState([]);
  const [selectedSchema, setSelectedSchema] = useState('');
  const [showFields, setShowFields] = useState(false);
  const [session, setSession] = useState({}); // To store the session data if needed
  const columns = ['Column1', 'Column2', 'Column3']; // Example column names, you might want to fetch them dynamically
  const operators = ['=', '!=', '<', '>', 'LIKE']; // Example operators

  const fetchSchemas = () => {
    fetch('http://localhost:5011/schemas')
      .then(response => response.json())
      .then(data => {
        setSchemas(data.schemas);
        setSelectedSchema('');
      })
      .catch(error => console.error('Error fetching schemas:', error));
  };

  const handleChangeSchema = (event) => {
    const schemaName = event.target.value;
    setSelectedSchema(schemaName);
    // Send request to select schema
    fetch('http://localhost:5011/schema', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ schema: schemaName }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === "Schema selected") {
          setShowFields(true); // Show dropdowns for filters
        } else {
          console.error(data.message); // Handle schema selection error if needed
        }
      })
      .catch(error => console.error('Error selecting schema:', error));
  };

  const handleFilterSubmit = (filterData) => {
    fetch('http://localhost:5011/filter/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(filterData),
    })
      .then(response => response.json())
      .then(data => {
        if (data.status === "Filter added") {
          // Handle successful addition of filters if necessary
          console.log(data.filters); // Here you can update the UI or state if needed
        } else {
          console.error(data.message); // Handle error if filtering fails
        }
      })
      .catch(error => console.error('Error adding filter:', error));
  };

  const handleReset = () => {
    setSelectedSchema('');
    setShowFields(false);
    setSchemas([]);
    // Optional: Call API to reset session
    fetch('http://localhost:5011/session/reset', {
      method: 'POST',
    });
  };

  return (
    <div className="container">
      <h1>Available Schemas</h1>
      {!showFields ? (
        <SchemaSelector
          schemas={schemas}
          selectedSchema={selectedSchema}
          onChange={handleChangeSchema}
          fetchSchemas={fetchSchemas}
        />
      ) : (
        <div>
          <h2>Selected Schema: {selectedSchema}</h2>
          <FilterFields
            columns={columns}
            operators={operators}
            count={3}
            onFilterSubmit={handleFilterSubmit}
          />
          <button onClick={handleReset} className="reset-btn">Reset</button>
        </div>
      )}
    </div>
  );
};

export default App;
