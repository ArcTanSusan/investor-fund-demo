import React from 'react';
import './App.css';
import { Formik, Field, Form, FieldArray } from 'formik';

const InvestorRow = ({ index }) => (
  <div style={{marginBottom: '20px'}}>
    <label htmlFor={`investor_amounts.${index}.name`}>Investor name</label>
    <Field id={`investor_amounts.${index}.name`} name={`investor_amounts.${index}.name`} placeholder="Name" />

    <label htmlFor={`investor_amounts.${index}.requested_amount`}> Requested amount </label>
    <Field id={`investor_amounts.${index}.requested_amount`} name={`investor_amounts.${index}.requested_amount`} type="text" placeholder="$ Requested amount" />

    <label htmlFor={`investor_amounts.${index}.average_amount`}> Average amount</label>
    <Field id={`investor_amounts.${index}.average_amount`} name={`investor_amounts.${index}.average_amount`} type="text" placeholder="$ Average amount" />
  </div>
);

function App() {

  const [results, setResults] = React.useState([]);
  const onClickProRate = async (values) => {
    const response = await fetch('http://127.0.0.1:8000/calculate?isComplexCalc=false', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(values),
    });
    const data = await response.json();
    setResults(Object.entries(data.result));
    console.log(results);
    return results;
  }

  const initialValues = {
    allocation_amount: '',
    investor_amounts: [
      {name: '', requested_amount: '', average_amount: ''}
    ],
  };

  return (
    <div className="App">
      <h1>A pro rating calculator</h1>

      <Formik
        initialValues={initialValues}
        onSubmit={onClickProRate}
      >
        {({ values }) => (
          <Form>
            <label htmlFor="allocation_amount">Total allocation</label>
            <Field id="allocation_amount" name="allocation_amount" placeholder="$ Allocation" />
            <h2>Investor breakdown</h2>
            <FieldArray name="investor_amounts">
              {({ push }) => (
                <>
                  {values.investor_amounts.map((investor, index) => (
                    <InvestorRow key={index} index={index} />
                  ))}
                  <button type="button" onClick={() => push({ name: '', requested_amount: '', average_amount: '' })}>
                    Add Investor
                  </button>
                </>
              )}
            </FieldArray>

            <hr />
            <button type="submit">Prorate</button>
          </Form>
        )}
      </Formik>

      <h1>Results</h1>
        {results.map(([name, amount]) => (
          <div key={name}>Investor {name} is allocated this amount: {amount}</div>
        ))}
    </div>
  );
}

export default App;