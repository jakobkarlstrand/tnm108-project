export interface IProbability {
    pos: number;
    neg: number;
}

export interface IArticle {
    title: string;
    image?: string;
    video?: string;
    description?: string;
    content?: string;
    link: string;
    probability_title: {
        pos: number;
        neg: number;
    };
    probability_description: {
        pos: number;
        neg: number;
    };
}
