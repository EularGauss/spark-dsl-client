import React from 'react';

const FieldGroup = ({ columns, operators, onColumnChange, onOperatorChange, onValueChange }) => (
  <div className="field-group">
    <select onChange={(e) => onColumnChange(e.target.value)}>
      <option value="">Select Column</option>
      {columns.map((col, index) => (
        <option key={index} value={col}>{col}</option>
      ))}
    </select>
    <select onChange={(e) => onOperatorChange(e.target.value)}>
      <option value="">Select Operator</option>
      {operators.map((operator, index) => (
        <option key={index} value={operator}>{operator}</option>
      ))}
    </select>
    <input type="text" placeholder="Enter value" onChange={(e) => onValueChange(e.target.value)} />
  </div>
);

export default FieldGroup;
