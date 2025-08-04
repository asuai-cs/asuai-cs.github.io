```jsx
// Project: Formal Verification Framework for RISC-V Security (React UI)
// 
// What it does:
// This React component creates a dashboard to display SymbiYosys verification results for riscv_core.v. It shows property pass/fail status, counterexamples, and coverage.
//
// How we built it:
// 1. Setup:
//    - Used React for dynamic UI with Tailwind CSS.
//    - Called WebAssembly (symbiyosys_wrapper.js) to run verification.
// 2. Data:
//    - Loaded test_vectors.json and simulated SymbiYosys output.
// 3. Testing:
//    - Tested with sample trace, verified pass/fail display.
//    - Checked responsiveness on mobile/desktop.
// 4. Usage:
//    - Run via index.html in browser.
//    - Host on Netlify for portfolio.
// 5. Notes:
//    - Click properties to see counterexamples.
//    - Expand test_vectors.json for more tests.

const { useState, useEffect } = React;

function App() {
  const [results, setResults] = useState([]);
  const [selectedProperty, setSelectedProperty] = useState(null);

  // Run verification
  useEffect(() => {
    fetch('test_vectors.json')
      .then(res => res.json())
      .then(vectors => {
        // Simulate SymbiYosys (WebAssembly)
        Module.runVerification(vectors).then(output => {
          setResults([
            { name: "no_user_write_supervisor", status: "PASS", counterexample: null },
            { name: "secure_boot_pc", status: "PASS", counterexample: null },
            { name: "no_invalid_privilege", status: "FAIL", counterexample: "PC=0x4, privilege=1" }
            // Simulated; real SymbiYosys output parsed here
          ]);
        });
      });
  }, []);

  return (
    <div className="flex h-screen">
      <div className="w-3/4 p-4">
        <h1 className="text-3xl font-bold mb-4">RISC-V Security Verification Dashboard</h1>
        <table className="w-full bg-gray-800 rounded">
          <thead>
            <tr>
              <th className="p-2">Property</th>
              <th className="p-2">Status</th>
              <th className="p-2">Details</th>
            </tr>
          </thead>
          <tbody>
            {results.map((res, i) => (
              <tr key={i} className="border-t border-gray-700">
                <td className="p-2">{res.name}</td>
                <td className="p-2">{res.status}</td>
                <td className="p-2">
                  <button
                    className="bg-blue-500 p-1 rounded"
                    onClick={() => setSelectedProperty(res)}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="w-1/4 p-4 bg-gray-800">
        <h2 className="text-xl font-semibold mb-4">Details</h2>
        {selectedProperty ? (
          <div>
            <p><strong>Property:</strong> {selectedProperty.name}</p>
            <p><strong>Status:</strong> {selectedProperty.status}</p>
            <p><strong>Counterexample:</strong> {selectedProperty.counterexample || "None"}</p>
          </div>
        ) : (
          <p>Select a property to view details.</p>
        )}
      </div>
    </div>
  );
}

ReactDOM.render(<App />, document.getElementById('root'));
```