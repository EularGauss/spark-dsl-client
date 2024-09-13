import React from 'react';

const SchemaSelector = ({ schemas, selectedSchema, onChange }) => (
  <div>
    <label htmlFor="schemaSelect">Choose a schema:</label>
    <select id="schemaSelect" value={selectedSchema} onChange={onChange}>
      <option value="">Select a schema...</option>
      {schemas.map((schema, index) => (
        <option key={index} value={schema}>{schema}</option>
      ))}
    </select>
  </div>
);

export default SchemaSelector;
