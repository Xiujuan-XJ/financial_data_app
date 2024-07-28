import React , {useState, useEffect} from 'react'

function App(){
  const [data, setData] = useState([{}]) //data is a state vairable and setData is a function to change the state of data
  
  useEffect(() => {
    fetch('/members').then(
        res=>res.json() //put response in json
    ).then(
      data=>{
        setData(data) //set data to jason
        console.log(data) //test on whether we receive it 
      }
    )
  },[]) //put empty array inside useEffect to make it run only once
  
  return (
      <div>
        {(typeof data.members === 'undefined')?( //check if data.members is undefined, means api has been fetched and we dont have the members yet
            <p>Loading...</p> // if it is undefined, display loading
          ):(
            data.members.map((member, i)=>( // otherwise, display the members
              <p key={i}> {member} </p> //display the member one by one
          ))
          )}
      </div>
  )
}

export default App