import React from "react";
import { IArticle } from "../types";
import Article from "./Article";

type Props = {
    articles: IArticle[];
};

function ListOfArticles({ articles }: Props) {
    return (
        <div
            style={{
                display: "flex",
                flexDirection: "column",
                gap: "50px",
                justifyContent: " center",
            }}
        >
            {articles
                .sort(
                    (a, b) =>
                        b.probability_description.pos -
                        a.probability_description.pos
                )
                .map((article) => {
                    return <Article key={article.title} article={article} />;
                })}
        </div>
    );
}

export default ListOfArticles;
