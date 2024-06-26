import { useEffect, useState } from "react";
import { Link, useLocation } from "react-router-dom";

const reqSender = require("./helpers/requests_sender")

function LogsRouter() {

    const jumpToBottom = ()=>{
        window.scrollTo(0, document.body.scrollHeight);
    }

    const [logs, setLogs] = useState("")

    const updateLogs = async () => {
        const fetchedLogs = await reqSender.getLogs()
        setLogs(fetchedLogs)
    }

    useEffect(() => {
        updateLogs()
    }, [])

    return (
        <div>
            <button onClick={jumpToBottom}>Jump To Buttom</button>
            <div style={{ whiteSpace: "pre-line" }}>
                {logs ? logs : "Loading Logs"}
            </div>
        </div>

    )
}

export default LogsRouter;