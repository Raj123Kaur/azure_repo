import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const current_date_time = Date.now()
    const [error, setError] = useState(null)
    // eslint-disable-next-line
	const getStats = () => {
	
        fetch(`http://messaging.eastus2.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>BookRide</th>
							<th>OrderFood</th>
						</tr>
						<tr>
							<td># OF: {stats['num_order_food_request']}</td>
							<td># BR: {stats['num_ride_request_request']}</td>
						</tr>
						
					</tbody>
                </table>
                <h3>Last Updated: {stats['last_updated']} {current_date_time}</h3>

            </div>
        )
    }
}
