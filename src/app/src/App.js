import './App.css';
import { useEffect,useState } from 'react';


export function App() {
  const [task, setTask] = useState("");
  const [list, setList] = useState([]);

  const fetchTodos = async () => {
    try {
      const res = await fetch("http://localhost:8000/todos");
      const data = await res.json();
      setList(data);
    } catch (err) {
      console.error("Error fetching todos: ", err);
    }
  };

  const handleStatus = async (id) => {
    setList(list.filter((item) => item._id !== id));
    try {
      await fetch(`http://localhost:8000/todos/${id}`, {
        method: "DELETE",
      });
    } catch (err) {
      console.error("Error deleting task: ", err);
    }
  }

  useEffect(() => {
    fetchTodos();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!task) {
      alert("Task cannot be empty");
      return; 
    }
    try {
      fetch("http://localhost:8000/todos/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ task }),
      });
      setTask("");
      fetchTodos();
    } catch (err) {
      console.error("Error adding todo: ", err);
    }
    console.log("Submitted task: ", task);
  }
  return (
    <div className="App">
      <div>
        <h1>List of TODOs</h1>
        <h3 color='blue'>Check the box to mark it as completed</h3>
        {list.length === 0 ? <p>No Tasks available</p> :
          <ul style={{"listStyle": "none"}}>
            {list.map((item, index) => (
                <li key={item._id}>
                  <input type="checkbox"
                  onChange={() => handleStatus(item._id)}
                  />
                  {item.task}
                </li>
            ))}

          </ul>
        }
      </div>
      <div>
        <h1>Create a ToDo</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label for="todo">ToDo: </label>
            <input type="text" value={task} onChange={ (e) => setTask(e.target.value)} />
          </div>
          <div style={{"marginTop": "5px"}}>
            <button>Add ToDo!</button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
