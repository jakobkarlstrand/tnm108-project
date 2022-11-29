import React from "react";
import logo from "./logo.svg";
import "./App.css";
import ListOfArticles from "./components/ListOfArticles";
import { IArticle } from "./types";

const ARTICLES = require("./kaggle.json") as IArticle[];

function App() {
    return (
        <div
            className="App"
            style={{ display: "flex", justifyContent: "center", width: "100%" }}
        >
            <ListOfArticles articles={ARTICLES} />
        </div>
    );
}

export default App;
