import React from 'react';

const SchemaSelector = ({ schemas, selectedSchema, onChange, fetchSchemas }) => (
  <div>
    <button onClick={fetchSchemas}>Select Schema</button>
    <label htmlFor="schemaSelect">Choose a schema:</label>
    <select
      id="schemaSelect"
      value={selectedSchema}
      onChange={onChange}
      disabled={schemas.length === 0}
    >
      <option value="">Select a schema...</option>
      {schemas.map((schema, index) => (
        <option key={index} value={schema}>{schema}</option>
      ))}
    </select>
  </div>
);

export default SchemaSelector;
