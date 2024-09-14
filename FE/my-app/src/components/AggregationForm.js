import React, { useState } from 'react';

const AggregationForm = ({ aggregations, columns, onAggregationSubmit }) => {
    const [selectedAggregation, setSelectedAggregation] = useState('');
    const [columnName, setColumnName] = useState('');

    const handleAggregationChange = (event) => {
        setSelectedAggregation(event.target.value);
        setColumnName(''); // Reset column name when changing aggregation
    };

// !selectedAggregation || (selectedAggregation === '')
    const handleColumnNameChange = (event) => {
        setColumnName(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        const aggregationData = {
            type: selectedAggregation,
            column: columnName // Include the column name if applicable
        };

        // Call the parent function to submit the aggregation
        onAggregationSubmit(aggregationData);

        // Clear the input fields after submission
        setSelectedAggregation('');
        setColumnName('');
    };

    const disableAggregationBtn = () => {
        var requiresColumn = aggregations.filter(e => e.name === selectedAggregation && e.requires_column);
        console.log('requiresColumn = ' + requiresColumn);
        if (requiresColumn.length === 0) return false;
        return !columnName;
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="aggregation-form-group">
                <div style={{ textAlign: 'center', marginBottom: '10px' }}>
                    <h1>Aggregate</h1>
                </div>
                <label htmlFor="aggregationSelect">Select Aggregation:</label>
                <select
                    id="aggregationSelect"
                    value={selectedAggregation}
                    onChange={handleAggregationChange}
                    required
                >
                    <option value="">Select Aggregation</option>
                    {aggregations.map((aggregation, index) => (
                        <option key={index} value={aggregation.name}>
                            {aggregation.name} {/* Display the name of the aggregation */}
                        </option>
                    ))}
                </select>

                {/* Display input for column name if aggregation requires it */}
               {selectedAggregation &&
                    aggregations.find(agg => agg.name === selectedAggregation)?.requires_column ? (
                    <div>
                        <label htmlFor="columnNameInput">Column Name:</label>
                        <select
                            id="columnNameInput"
                            value={columnName}
                            onChange={handleColumnNameChange}
                            required
                        >
                            <option value="">Select Column</option>
                            {columns.map((column, index) => (
                                <option key={index} value={column}>
                                    {column} {/* Display column name */}
                                </option>
                            ))}
                        </select>
                    </div>
                ) : null}
                <button type="submit" disabled={disableAggregationBtn()}>
                    Add Aggregation
                </button>
            </div>
        </form>
    );
};

export default AggregationForm;
