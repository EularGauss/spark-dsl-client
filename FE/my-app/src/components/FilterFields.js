import React, { useState } from 'react';
import FieldGroup from './FieldGroup';

const FilterFields = ({ columns, operators, count, onFilterSubmit }) => {
  // A state to track the filters being added
  const [filters, setFilters] = useState(
    Array(count).fill({ column: '', operator: '', value: '' })
  );

  const handleChange = (index, field, value) => {
    const updatedFilters = [...filters];
    updatedFilters[index][field] = value;
    setFilters(updatedFilters);
  };

  const handleAddFilter = (index) => {
    const { column, operator, value } = filters[index];
    if (column && operator && value) {
      onFilterSubmit({ name: column, operator, value, type: "ExampleType" }); // Replace "ExampleType" with your logic
    } else {
      alert('Please fill in all fields');
    }
  };

  return (
    <div>
      {filters.map((_, index) => (
        <div key={index} className="field-set">
          <FieldGroup
            columns={columns}
            operators={operators}
            onColumnChange={(value) => handleChange(index, 'column', value)}
            onOperatorChange={(value) => handleChange(index, 'operator', value)}
            onValueChange={(value) => handleChange(index, 'value', value)}
          />
          <button onClick={() => handleAddFilter(index)} className="add-filter-btn">Add Filter</button>
        </div>
      ))}
    </div>
  );
};

export default FilterFields;
