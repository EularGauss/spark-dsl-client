import React, { useState } from 'react';

const FilterForm = ({ columns, columnDetails, onFilterSubmit }) => {
    const [selectedColumn, setSelectedColumn] = useState('');
    const [selectedOperation, setSelectedOperation] = useState('');
    const [value, setValue] = useState('');

    const handleColumnChange = (event) => {
        setSelectedColumn(event.target.value);
        setSelectedOperation(''); // Reset operations when the column changes
        setValue(''); // Reset value when changing the column
    };

    const handleOperationChange = (event) => {
        setSelectedOperation(event.target.value);
    };

    const handleValueChange = (event) => {
        setValue(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        // Prepare the filter data to submit
        const filterData = {
            name: selectedColumn,
            operator: selectedOperation,
            value: value,
            type: columnDetails[selectedColumn]?.type // Get the type based on the selected column
        };

        onFilterSubmit(filterData); // Pass the filter data to parent
    };

    // Determine allowed operators for the selected column
    const allowedOps = selectedColumn ? columnDetails[selectedColumn].allowed_operators : [];
    const columnType = selectedColumn ? columnDetails[selectedColumn].type : null;

    // Check if column type is a union type or enum type
    let derivedAllowedOps = allowedOps;
    let enumValues = [];

    if (columnType) {
        if (columnType.type === "union" && columnType.types) {
            derivedAllowedOps = [];
            columnType.types.forEach(type => {
                const opsForType = columnDetails[type].allowed_operators;
                opsForType.forEach(operator => {
                    if (!derivedAllowedOps.some(op => op[0] === operator[0])) {
                        derivedAllowedOps.push(operator);
                    }
                });
            });
        } else if (columnType.type === "enum" && columnType.values) {
            enumValues = columnType.values; // Get enum values for the dropdown
        }
    }


 return (
    <form onSubmit={handleSubmit}>
        <div className="filter-form-group">
            <label htmlFor="columnSelect">Column Name:</label>
            <select id="columnSelect" value={selectedColumn} onChange={handleColumnChange} required>
                <option value="">Select Column</option>
                {columns.map((column, index) => {
                    const columnTypeDetails = columnDetails[column];
                    const displayType = columnTypeDetails?.type?.type ? columnTypeDetails.type.type : columnTypeDetails.type;

                    return (
                        <option key={index} value={column}>
                            {column} ({displayType})  {/* Display column name and type */}
                        </option>
                    );
                })}
            </select>

            <label htmlFor="operationSelect">Operation:</label>
            <select id="operationSelect" value={selectedOperation} onChange={handleOperationChange} required>
                <option value="">Select Operation</option>
                {derivedAllowedOps.map((operator, index) => (
                    <option key={index} value={operator[0]}>{operator[0]}</option>
                ))}
            </select>

            {/* Conditional rendering for enum values */}
            {columnType && columnType.type === "enum" ? (
                <>
                    <label htmlFor="valueSelect">Enum Values:</label>
                    <select id="valueSelect" value={value} onChange={handleValueChange} required>
                        <option value="">Select Value</option>
                        {enumValues.map((enumValue, index) => (
                            <option key={index} value={enumValue}>{enumValue}</option>
                        ))}
                    </select>
                </>
            ) : (
                <>
                    <label htmlFor="valueInput">Value:</label>
                    <input
                        type="text"
                        id="valueInput"
                        value={value}
                        onChange={handleValueChange}
                        placeholder="Enter value"
                        required
                    />
                </>
            )}

            <button type="submit">Submit Filter</button>
        </div>
    </form>
);
}
export default FilterForm;
