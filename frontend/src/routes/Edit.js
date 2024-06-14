import React, { useEffect, useState } from "react";
import EmptyFiles from './helpers_components/EmptyFiles'
import LoadingFiles from "./helpers_components/LoadingFiles";

const reqSender = require("./helpers/requests_sender")

function Edit() {

    const [animeList, setAnimeList] = useState([]);
    const [loading, setLoading] = useState(true)

    var requestLoading = false

    const fetchAnimeFunction = async () => {
        // requestLoading is used to avoid sending
        // requests while the previous request is
        // still pending

        if (requestLoading) {
            return
        }

        requestLoading = true

        const animes = await reqSender.getAnimes()
        setAnimeList(animes)

        setLoading(false)
        requestLoading = false
    }

    const removeAnime = async (name) => {
        const response = await reqSender.removeAnime(name)
        alert(JSON.stringify(response))
        fetchAnimeFunction() // to refresh immedietly after a remove
    }

    useEffect(() => {
        fetchAnimeFunction()

        const number = setInterval(() => {
            fetchAnimeFunction()
        }, 5000)

        console.log(`created a new interval for fetchAnimeFunction: ${number}`)


        // when the component is 'unmount'ed the return function is executed.
        // so, we clear the interval to avoid creating multiple intervals
        return () => {
            console.log(`clearInterval(${number}) for fetchAnimeFunction`)
            clearInterval(number)
        }

    }, [])

    if (loading) {
        return <LoadingFiles />
    }

    if (animeList.length === 0) {
        return <EmptyFiles />
    }



    return <div>

        <div className="all-animes-container">
            {
                animeList.map((anime) => {
                    return (
                        <div className="anime-container" key={anime.name}>
                            <div className="anime-name" title="Click To Show Keyword" onClick={
                                () => {
                                    alert(anime.keyword)
                                }
                            }>{anime.name}</div>
                            <div className="anime-path" title="Path">{anime.path}</div>
                            <div className="anime-delete-button-container">
                                <button onClick={
                                    () => {
                                        removeAnime(anime.name)
                                    }
                                } className="anime-delete-button">x</button>
                            </div>
                        </div>
                    )
                })
            }

        </div>

    </div>
}

export default Edit;