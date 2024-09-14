import React, { useState } from 'react';

const TransformationForm = ({ transformations, onTransformationSubmit }) => {
    const [selectedTransformation, setSelectedTransformation] = useState('');
    const [lambdaFunction, setLambdaFunction] = useState('');

    const handleTransformationChange = (event) => {
        const { value } = event.target;
        setSelectedTransformation(value);
        setLambdaFunction(''); // Clear the lambda function input when changing transformation
    };

    const handleLambdaChange = (event) => {
        setLambdaFunction(event.target.value);
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        const transformationData = {
            type: selectedTransformation,
            function: lambdaFunction // Include the lambda function if applicable
        };

        // Call the parent function to submit the transformation
        onTransformationSubmit(transformationData);

        // Clear the input fields after submission
        setSelectedTransformation('');
        setLambdaFunction('');
    };

    return (
        <form onSubmit={handleSubmit}>
            <div className="transformation-form-group">
                <div style={{ textAlign: 'center', marginBottom: '10px' }}>
                    <h1>Transform</h1>
                </div>
                <label htmlFor="transformationSelect">Select Transformation:</label>
                <select
                    id="transformationSelect"
                    value={selectedTransformation}
                    onChange={handleTransformationChange}
                    required
                >
                    <option value="">Select Transformation</option>
                    {transformations.map((transformation, index) => (
                        <option key={index} value={transformation.name}>
                            {transformation.name} {/* Display the name of the transformation */}
                        </option>
                    ))}
                </select>

                {/* Display the input for the lambda function only if the selected transformation requires it */}
               {selectedTransformation && (
                    // Check if the selected transformation requires a lambda function
                    transformations.find(t => t.name === selectedTransformation)?.requires_lambda ? (
                        <div>
                            <label htmlFor="lambdaFunctionInput">Scala Function:</label>
                            <input
                                type="text"
                                id="lambdaFunctionInput"
                                value={lambdaFunction}
                                onChange={handleLambdaChange}
                                placeholder="Enter Scala function (if required)"
                                required // Optional based on your application needs
                            />
                        </div>
                    ) : null // Do not render anything if it doesn't require a lambda function
                )}
                <button
                    type="submit"
                    disabled={
                        !selectedTransformation ||
                        (transformations.find(t => t.name === selectedTransformation)?.requires_lambda && !lambdaFunction)
                    }
                >
                    Add Transformation
                </button>
            </div>
        </form>
    );
};

export default TransformationForm;
