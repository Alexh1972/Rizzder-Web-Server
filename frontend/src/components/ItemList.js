// import React, { useEffect, useState } from 'react';
// import api from '../services/api'; // Adjust the path to your `api.js`
//
// function ItemList() {
//   const [items, setItems] = useState([]);
//
//   // Fetch data when the component mounts
//   useEffect(() => {
//     async function fetchData() {
//       try {
//         const response = await api.get('/items'); // Adjust endpoint
//         setItems(response.data);
//       } catch (error) {
//         console.error('Error fetching data:', error);
//       }
//     }
//
//     fetchData();
//   }, []); // Empty dependency array ensures this runs once after the component mounts
//
//   return (
//     <div>
//       <h1>Items</h1>
//       <ul>
//         {items.map(item => (
//           <li key={item.id}>{item.name}</li>
//         ))}
//       </ul>
//     </div>
//   );
// }
//
// export default ItemList;
import React from 'react';
import LogoRizzder from '../assets/LogoRizzder.png'; // Adjust the path as needed

const ItemList = () => {
  return (
    <div>
      <img src={LogoRizzder} alt="LogoRizzder" className="logo-img" />
    </div>
  );
};

export default ItemList;
