import React from "react";
import { IArticle } from "../types";

const IMAGE_URL =
    "https://nbhc.ca/sites/default/files/styles/article/public/default_images/news-default-image%402x_0.png?itok=B4jML1jF";

type Props = {
    article: IArticle;
};

function Article({ article }: Props) {
    console.log(article.video);
    return (
        <div
            style={{
                maxWidth: "700px",
                backgroundColor: "white",
                borderRadius: "4px",
                boxShadow: "0px 1px 2px 0px rgba(0,0,0,0.15)",
            }}
        >
            <div>
                <img
                    style={{ width: "100%", objectFit: "cover" }}
                    src={article.image ?? IMAGE_URL}
                    alt="News header"
                />
            </div>
            <div style={{ padding: "0 2rem" }}>
                <a
                    style={{ textDecoration: "none", color: "unset" }}
                    href={article.link}
                    target="_blank"
                    rel="noreferrer"
                >
                    <h2
                        className="headline"
                        style={{ fontSize: "36px", fontWeight: "bold" }}
                    >
                        {article.title}
                    </h2>
                </a>

                <p>{article.description || article.content?.slice(0, 200)}</p>
                <p>
                    Positive index:{" "}
                    <b>{`${article.probability_description.pos.toFixed(2)}`}</b>
                </p>
            </div>
        </div>
    );
}

export default Article;
