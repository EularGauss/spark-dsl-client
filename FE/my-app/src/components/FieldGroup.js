import React, { useState } from 'react';

const AggregationForm = ({ aggregations, onAggregationSubmit }) => {
    const [selectedAggregation, setSelectedAggregation] = useState('');
    const [columnName, setColumnName] = useState('');

    const handleAggregationChange = (event) => {
        setSelectedAggregation(event.target.value);
        setColumnName(''); // Reset column name when changing aggregation
    };

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

    return (
        <form onSubmit={handleSubmit}>
            <div className="aggregation-form-group">
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
                {selectedAggregation && (
                    <div>
                        <label htmlFor="columnNameInput">Column Name:</label>
                        <input
                            type="text"
                            id="columnNameInput"
                            value={columnName}
                            onChange={handleColumnNameChange}
                            placeholder="Enter column name"
                            required={selectedAggregation !== "groupBy"} // Example: groupBy might not need a column
                        />
                    </div>
                )}

                <button type="submit" disabled={!selectedAggregation || (selectedAggregation !== "groupBy" && !columnName)}>
                    Add Aggregation
                </button>
            </div>
        </form>
    );
};

export default AggregationForm;
