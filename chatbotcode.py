import os
import openai
import pandas as pd
import spacy
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

nlp = spacy.load('fr_core_news_md')

questions = [
    "Quelles sont vos compétences principales ?",
    "Pouvez-vous décrire vos compétences principales ?",
    "Quelles sont les compétences clés que vous maîtrisez ?",
    "Quels sont vos principaux atouts professionnels ?",
    
    "Quelle est votre formation ?",
    "Pouvez-vous me parler de votre parcours académique ?",
    "Quelle est votre formation initiale ?",
    "Quel est votre parcours en termes de formation ?",
    
    "Pouvez-vous me parler d'un projet concret lié à l'apprentissage automatique ?",
    "Avez-vous réalisé un projet en lien avec le machine learning ?",
    "Pouvez-vous détailler un projet pratique que vous avez mené en IA ?",
    "Pouvez-vous donner un exemple d'application concrète de l'apprentissage automatique dans vos travaux ?",
    
    "Quels défis professionnels avez-vous surmontés ?",
    "Quels types de défis professionnels avez-vous dû relever ?",
    "Pouvez-vous partager des exemples de défis professionnels que vous avez surmontés ?",
    "Quels obstacles avez-vous rencontrés dans votre carrière et comment les avez-vous surmontés ?",
    
    "Comment gérez-vous la pression et les délais serrés ?",
    "Comment faites-vous face à la pression et aux contraintes de temps ?",
    "Comment gérez-vous des situations sous pression avec des délais courts ?",
    "Quelle est votre approche pour gérer des délais serrés et un environnement stressant ?",

    "Quelles technologies et outils utilisez-vous dans vos projets ?",
    "Quels outils techniques utilisez-vous dans vos projets d'IA ?",
    "Quelles sont les technologies que vous maîtrisez pour vos projets ?",
    "Quels sont les outils et langages que vous employez dans vos développements ?",
    
    "Comment votre profil peut-il apporter de la valeur à une entreprise ?",
    "En quoi votre profil serait-il un atout pour notre entreprise ?",
    "Quels bénéfices pouvez-vous apporter à une entreprise avec vos compétences ?",
    "Comment vos compétences stratégiques et techniques peuvent-elles améliorer une entreprise ?",

    "Comment alliez-vous stratégie et intelligence artificielle dans votre approche ?",
    "Comment intégrez-vous l'IA dans vos stratégies professionnelles ?",
    "Pouvez-vous expliquer comment vous associez la stratégie d'entreprise à l'intelligence artificielle ?",
    "Comment combinez-vous l’IA et la stratégie dans votre méthodologie de travail ?",

    "Quels sont vos objectifs à long terme ?",
    "Quels sont vos projets à long terme dans le domaine de l'IA ?",
    "Quels sont vos objectifs de carrière sur le long terme ?",
    "Quels sont vos projets futurs à l'échelle professionnelle ?",

    "Pourquoi pensez-vous que votre profil est adapté à notre entreprise ?",
    "Qu'est-ce qui rend votre profil pertinent pour notre entreprise ?",
    "En quoi vos compétences correspondent-elles à nos besoins ?",
    "Pourquoi votre parcours fait-il de vous le candidat idéal pour notre entreprise ?",

    "Comment assurez-vous une bonne communication entre les équipes techniques et non techniques ?",
    "Comment facilitez-vous la communication entre les équipes techniques et les autres départements ?",
    "Comment vous assurez-vous que la collaboration entre les équipes techniques et non techniques soit fluide ?",
    "Quelles méthodes utilisez-vous pour assurer une bonne communication entre équipes multidisciplinaires ?",

    "Quel type de projet vous motive le plus ?",
    "Quels sont les projets qui vous inspirent le plus ?",
    "Quel type de projet éveille votre motivation professionnelle ?",
    "Quels projets vous stimulent et vous engagent le plus professionnellement ?",
    
    "Comment vous maintenez-vous à jour avec les avancées technologiques ?",
    "Comment assurez-vous une veille sur les nouvelles technologies ?",
    "Quelle méthode utilisez-vous pour rester informé des innovations technologiques ?",
    "Comment vous tenez-vous au courant des évolutions dans votre domaine ?",

    "Quelle est votre méthode pour résoudre des problèmes complexes ?",
    "Quelle approche adoptez-vous pour traiter des problèmes difficiles ?",
    "Comment procédez-vous lorsque vous êtes confronté à des problèmes complexes ?",
    "Quelle est votre méthodologie pour analyser et résoudre des défis complexes ?",

    "Comment adaptez-vous vos solutions en fonction des besoins spécifiques de l’entreprise ?",
    "Comment personnalisez-vous vos solutions pour répondre aux besoins spécifiques d'une entreprise ?",
    "Comment adaptez-vous vos stratégies aux exigences particulières d'une entreprise ?",
    "Quelle est votre approche pour ajuster vos solutions en fonction des besoins précis de chaque entreprise ?"

    "Comment vos expériences internationales influencent-elles votre travail ?",
    "De quelle manière vos voyages influencent-ils votre approche professionnelle ?",
    "Comment vos expériences à l'étranger enrichissent-elles vos projets ?",
    "Quel impact vos expériences internationales ont-elles sur votre manière de travailler ?",

    "Comment avez-vous développé votre capacité d'adaptation ?",
    "Pouvez-vous décrire une situation où vous avez dû vous adapter rapidement ?",
    "Comment votre capacité d'adaptation vous aide-t-elle dans votre travail ?",
    "Qu'est-ce qui vous permet de vous adapter à des environnements changeants ?",

    "Pourquoi avez-vous choisi de vous spécialiser dans l'intelligence artificielle ?",
    "Qu'est-ce qui vous a attirée vers l'apprentissage automatique et l'IA ?",
    "Pourquoi l'IA vous passionne-t-elle ?",
    "Qu'est-ce qui vous motive dans le domaine de l'intelligence artificielle ?",

    "Comment gérez-vous le contrôle budgétaire dans vos projets ?",
    "Quelle est votre méthode pour respecter un budget de projet ?",
    "Comment optimisez-vous les ressources financières dans vos projets ?",
    "Comment assurez-vous un suivi rigoureux des dépenses dans vos projets ?",

    "Comment utilisez-vous les données pour optimiser la performance ?",
    "Quelle est votre approche de l'analyse de données pour améliorer les performances ?",
    "Comment les données vous aident-elles à prendre des décisions dans vos projets ?",
    "Comment vous servez-vous des KPIs pour optimiser vos projets ?",

    "Quelle est votre vision de l'avenir de la transformation digitale ?",
    "Comment voyez-vous l'évolution de la digitalisation des entreprises ?",
    "Quel est l'impact de la transformation digitale selon vous ?",
    "Quelle est votre vision de la transformation numérique dans les prochaines années ?",

    "Comment l'intelligence artificielle peut-elle améliorer les processus organisationnels ?",
    "Comment l'IA peut-elle être un atout pour l'organisation interne des entreprises ?",
    "Pouvez-vous expliquer comment l'IA optimise les processus opérationnels ?",
    "Quel rôle l'IA peut-elle jouer dans l'amélioration des processus d'une entreprise ?",

    "Quels aspects de votre profil vous distinguent de vos concurrents ?",
    "En quoi votre parcours est-il unique par rapport aux autres candidats ?",
    "Quelles compétences vous différencient de vos pairs dans votre domaine ?",
    "Pourquoi pensez-vous que votre profil est particulièrement distinctif ?",

    "Comment avez-vous géré une équipe pour la première fois ?",
    "Pouvez-vous partager une expérience de gestion d'équipe ?",
    "Comment avez-vous surmonté les défis lors de votre première expérience de management ?",
    "Quelle a été votre stratégie pour gérer votre première équipe ?",

    "Comment appliquez-vous vos connaissances en IA pour résoudre des problématiques sociétales ?",
    "Pouvez-vous donner un exemple d'application de l'IA pour des projets à impact social ?",
    "Comment l'IA peut-elle être utilisée pour résoudre des problèmes sociaux ?",
    "Quel est le potentiel de l'IA pour améliorer la société, selon vous ?"
]
answers = [
    "Mes compétences principales incluent l'élaboration de stratégie digitale marketing et communication, le développement d'outils d'intelligence artificielle, l'apprentissage automatique, l'optimisation des performances à travers l’automatisation et la gestion de projet.",
    "Mes compétences principales incluent l'élaboration de stratégie digitale marketing et communication, le développement d'outils d'intelligence artificielle, l'apprentissage automatique, l'optimisation des performances à travers l’automatisation et la gestion de projet.",
    "Mes compétences principales incluent l'élaboration de stratégie digitale marketing et communication, le développement d'outils d'intelligence artificielle, l'apprentissage automatique, l'optimisation des performances à travers l’automatisation et la gestion de projet.",
    "Mes compétences principales incluent l'élaboration de stratégie digitale marketing et communication, le développement d'outils d'intelligence artificielle, l'apprentissage automatique, l'optimisation des performances à travers l’automatisation et la gestion de projet.",

    "Issue d'une école de commerce, j'ai ensuite été diplômée d'un MBA Chief Digital Officer. Je suis actuellement une formation en apprentissage automatique via une spécialisation de Stanford University et DeepLearning.ai.",
    "Issue d'une école de commerce, j'ai ensuite été diplômée d'un MBA Chief Digital Officer. Je suis actuellement une formation en apprentissage automatique via une spécialisation de Stanford University et DeepLearning.ai.",
    "Issue d'une école de commerce, j'ai ensuite été diplômée d'un MBA Chief Digital Officer. Je suis actuellement une formation en apprentissage automatique via une spécialisation de Stanford University et DeepLearning.ai.",
    "Issue d'une école de commerce, j'ai ensuite été diplômée d'un MBA Chief Digital Officer. Je suis actuellement une formation en apprentissage automatique via une spécialisation de Stanford University et DeepLearning.ai.",

    "J’ai récemment développé un chatbot qui permet d’en savoir plus sur mon profil de manière ludique. En parallèle, je travaille sur un outil de gestion de projet basé sur le machine learning, qui aide à prioriser les tâches et à allouer les ressources. Ces projets montrent ma capacité à appliquer mes apprentissages à des solutions concrètes.",
    "J’ai récemment développé un chatbot qui permet d’en savoir plus sur mon profil de manière ludique. En parallèle, je travaille sur un outil de gestion de projet basé sur le machine learning, qui aide à prioriser les tâches et à allouer les ressources. Ces projets montrent ma capacité à appliquer mes apprentissages à des solutions concrètes.",
    "J’ai récemment développé un chatbot qui permet d’en savoir plus sur mon profil de manière ludique. En parallèle, je travaille sur un outil de gestion de projet basé sur le machine learning, qui aide à prioriser les tâches et à allouer les ressources. Ces projets montrent ma capacité à appliquer mes apprentissages à des solutions concrètes.",
    "J’ai récemment développé un chatbot qui permet d’en savoir plus sur mon profil de manière ludique. En parallèle, je travaille sur un outil de gestion de projet basé sur le machine learning, qui aide à prioriser les tâches et à allouer les ressources. Ces projets montrent ma capacité à appliquer mes apprentissages à des solutions concrètes.",

    "J’ai surmonté plusieurs défis, notamment lors de projets où les délais de réalisation étaient très courts, il fallait donc faire preuve de sang-froid et exceller en communication interne. J'ai aussi géré de petites équipes multidisciplinaires d'apprentis en assurant une communication fluide et des résultats optimaux.",
    "J’ai surmonté plusieurs défis, notamment lors de projets où les délais de réalisation étaient très courts, il fallait donc faire preuve de sang-froid et exceller en communication interne. J'ai aussi géré de petites équipes multidisciplinaires d'apprentis en assurant une communication fluide et des résultats optimaux.",
    "J’ai surmonté plusieurs défis, notamment lors de projets où les délais de réalisation étaient très courts, il fallait donc faire preuve de sang-froid et exceller en communication interne. J'ai aussi géré de petites équipes multidisciplinaires d'apprentis en assurant une communication fluide et des résultats optimaux.",
    "J’ai surmonté plusieurs défis, notamment lors de projets où les délais de réalisation étaient très courts, il fallait donc faire preuve de sang-froid et exceller en communication interne. J'ai aussi géré de petites équipes multidisciplinaires d'apprentis en assurant une communication fluide et des résultats optimaux.",

    "Je m'assure avant toute chose d'avoir parfaitement bien compris les besoins et les attentes. J’organise mon travail de manière rigoureuse en priorisant les tâches critiques. Ma capacité à anticiper les problèmes et à adapter rapidement les solutions me permet de gérer efficacement la pression.",
    "Je m'assure avant toute chose d'avoir parfaitement bien compris les besoins et les attentes. J’organise mon travail de manière rigoureuse en priorisant les tâches critiques. Ma capacité à anticiper les problèmes et à adapter rapidement les solutions me permet de gérer efficacement la pression.",
    "Je m'assure avant toute chose d'avoir parfaitement bien compris les besoins et les attentes. J’organise mon travail de manière rigoureuse en priorisant les tâches critiques. Ma capacité à anticiper les problèmes et à adapter rapidement les solutions me permet de gérer efficacement la pression.",
    "Je m'assure avant toute chose d'avoir parfaitement bien compris les besoins et les attentes. J’organise mon travail de manière rigoureuse en priorisant les tâches critiques. Ma capacité à anticiper les problèmes et à adapter rapidement les solutions me permet de gérer efficacement la pression.",

    "Pour le développement de solutions : j'utilise Python pour la programmation, TensorFlow, scikit-learn ou autres outils pertinents dans le cadre d'un projet d'apprentissage automatique, et Flask pour déployer et utiliser. Pour l'automatisation : soit une solution IA personnalisée, soit des applications comme Zapier. Pour la gestion de projet : j'ai une bonne maîtrise de Notion et Monday.com.",
    "Pour le développement de solutions : j'utilise Python pour la programmation, TensorFlow, scikit-learn ou autres outils pertinents dans le cadre d'un projet d'apprentissage automatique, et Flask pour déployer et utiliser. Pour l'automatisation : soit une solution IA personnalisée, soit des applications comme Zapier. Pour la gestion de projet : j'ai une bonne maîtrise de Notion et Monday.com.",
    "Pour le développement de solutions : j'utilise Python pour la programmation, TensorFlow, scikit-learn ou autres outils pertinents dans le cadre d'un projet d'apprentissage automatique, et Flask pour déployer et utiliser. Pour l'automatisation : soit une solution IA personnalisée, soit des applications comme Zapier. Pour la gestion de projet : j'ai une bonne maîtrise de Notion et Monday.com.",
    "Pour le développement de solutions : j'utilise Python pour la programmation, TensorFlow, scikit-learn ou autres outils pertinents dans le cadre d'un projet d'apprentissage automatique, et Flask pour déployer et utiliser. Pour l'automatisation : soit une solution IA personnalisée, soit des applications comme Zapier. Pour la gestion de projet : j'ai une bonne maîtrise de Notion et Monday.com.",

    "Mon double profil, qui combine expertise stratégique et compétences techniques, me permet d’apporter une réelle valeur ajoutée. Je suis capable de diagnostiquer les besoins d'une entreprise et d'y répondre avec des solutions innovantes basées sur l’intelligence artificielle. Mon approche orientée résultats garantit également des projets livrés de manière fluide et efficace.",
    "Mon double profil, qui combine expertise stratégique et compétences techniques, me permet d’apporter une réelle valeur ajoutée. Je suis capable de diagnostiquer les besoins d'une entreprise et d'y répondre avec des solutions innovantes basées sur l’intelligence artificielle. Mon approche orientée résultats garantit également des projets livrés de manière fluide et efficace.",
    "Mon double profil, qui combine expertise stratégique et compétences techniques, me permet d’apporter une réelle valeur ajoutée. Je suis capable de diagnostiquer les besoins d'une entreprise et d'y répondre avec des solutions innovantes basées sur l’intelligence artificielle. Mon approche orientée résultats garantit également des projets livrés de manière fluide et efficace.",
    "Mon double profil, qui combine expertise stratégique et compétences techniques, me permet d’apporter une réelle valeur ajoutée. Je suis capable de diagnostiquer les besoins d'une entreprise et d'y répondre avec des solutions innovantes basées sur l’intelligence artificielle. Mon approche orientée résultats garantit également des projets livrés de manière fluide et efficace.",

    "J’utilise l’intelligence artificielle comme un levier d’optimisation dans mes stratégies digitales. Par exemple, j’intègre des outils d'IA pour automatiser et améliorer la performance des campagnes de communication, tout en optimisant les processus organisationnels à travers des solutions d’automatisation.",
    "J’utilise l’intelligence artificielle comme un levier d’optimisation dans mes stratégies digitales. Par exemple, j’intègre des outils d'IA pour automatiser et améliorer la performance des campagnes de communication, tout en optimisant les processus organisationnels à travers des solutions d’automatisation.",
    "J’utilise l’intelligence artificielle comme un levier d’optimisation dans mes stratégies digitales. Par exemple, j’intègre des outils d'IA pour automatiser et améliorer la performance des campagnes de communication, tout en optimisant les processus organisationnels à travers des solutions d’automatisation.",
    "J’utilise l’intelligence artificielle comme un levier d’optimisation dans mes stratégies digitales. Par exemple, j’intègre des outils d'IA pour automatiser et améliorer la performance des campagnes de communication, tout en optimisant les processus organisationnels à travers des solutions d’automatisation.",

    "À long terme, je souhaite participer à des projets à fort impact en exploitant le potentiel de l'intelligence artificielle pour transformer des idées en solutions concrètes. Mon ambition est d’utiliser l’IA pour améliorer la qualité de vie et contribuer à un avenir plus durable.",
    "À long terme, je souhaite participer à des projets à fort impact en exploitant le potentiel de l'intelligence artificielle pour transformer des idées en solutions concrètes. Mon ambition est d’utiliser l’IA pour améliorer la qualité de vie et contribuer à un avenir plus durable.",
    "À long terme, je souhaite participer à des projets à fort impact en exploitant le potentiel de l'intelligence artificielle pour transformer des idées en solutions concrètes. Mon ambition est d’utiliser l’IA pour améliorer la qualité de vie et contribuer à un avenir plus durable.",
    "À long terme, je souhaite participer à des projets à fort impact en exploitant le potentiel de l'intelligence artificielle pour transformer des idées en solutions concrètes. Mon ambition est d’utiliser l’IA pour améliorer la qualité de vie et contribuer à un avenir plus durable.",

    "Je suis proactive, adaptable et orientée résultats. Mon approche stratégique, couplée à une compréhension approfondie des technologies émergentes comme l’IA, me permet de proposer des solutions novatrices qui apportent une valeur ajoutée significative. De plus, mon expérience en gestion de projet me permet de m'assurer que les projets sont menés de manière fluide et efficace.",
    "Je suis proactive, adaptable et orientée résultats. Mon approche stratégique, couplée à une compréhension approfondie des technologies émergentes comme l’IA, me permet de proposer des solutions novatrices qui apportent une valeur ajoutée significative. De plus, mon expérience en gestion de projet me permet de m'assurer que les projets sont menés de manière fluide et efficace.",
    "Je suis proactive, adaptable et orientée résultats. Mon approche stratégique, couplée à une compréhension approfondie des technologies émergentes comme l’IA, me permet de proposer des solutions novatrices qui apportent une valeur ajoutée significative. De plus, mon expérience en gestion de projet me permet de m'assurer que les projets sont menés de manière fluide et efficace.",
    "Je suis proactive, adaptable et orientée résultats. Mon approche stratégique, couplée à une compréhension approfondie des technologies émergentes comme l’IA, me permet de proposer des solutions novatrices qui apportent une valeur ajoutée significative. De plus, mon expérience en gestion de projet me permet de m'assurer que les projets sont menés de manière fluide et efficace.",

    "Grâce à ma double formation, je peux facilement faire le lien entre les équipes techniques et non techniques. Je m'assure que les besoins de chaque partie sont bien compris et que la communication est fluide, garantissant ainsi une exécution de projet sans accroc.",
    "Grâce à ma double formation, je peux facilement faire le lien entre les équipes techniques et non techniques. Je m'assure que les besoins de chaque partie sont bien compris et que la communication est fluide, garantissant ainsi une exécution de projet sans accroc.",
    "Grâce à ma double formation, je peux facilement faire le lien entre les équipes techniques et non techniques. Je m'assure que les besoins de chaque partie sont bien compris et que la communication est fluide, garantissant ainsi une exécution de projet sans accroc.",
    "Grâce à ma double formation, je peux facilement faire le lien entre les équipes techniques et non techniques. Je m'assure que les besoins de chaque partie sont bien compris et que la communication est fluide, garantissant ainsi une exécution de projet sans accroc.",

    "Je suis particulièrement motivée par les projets qui permettent d’exploiter les nouvelles technologies comme l’IA pour résoudre des problèmes réels. J’aime les projets à fort impact, où je peux voir les résultats concrets et la valeur ajoutée apportée à l’entreprise.",
    "Je suis particulièrement motivée par les projets qui permettent d’exploiter les nouvelles technologies comme l’IA pour résoudre des problèmes réels. J’aime les projets à fort impact, où je peux voir les résultats concrets et la valeur ajoutée apportée à l’entreprise.",
    "Je suis particulièrement motivée par les projets qui permettent d’exploiter les nouvelles technologies comme l’IA pour résoudre des problèmes réels. J’aime les projets à fort impact, où je peux voir les résultats concrets et la valeur ajoutée apportée à l’entreprise.",
    "Je suis particulièrement motivée par les projets qui permettent d’exploiter les nouvelles technologies comme l’IA pour résoudre des problèmes réels. J’aime les projets à fort impact, où je peux voir les résultats concrets et la valeur ajoutée apportée à l’entreprise.",

    "Je consacre du temps chaque semaine à la veille technologique, je suis des formations en ligne et participe à des webinaires. De plus, je suis des blogs spécialisés et m’implique dans des communautés professionnelles pour être toujours à la pointe des dernières avancées.",
    "Je consacre du temps chaque semaine à la veille technologique, je suis des formations en ligne et participe à des webinaires. De plus, je suis des blogs spécialisés et m’implique dans des communautés professionnelles pour être toujours à la pointe des dernières avancées.",
    "Je consacre du temps chaque semaine à la veille technologique, je suis des formations en ligne et participe à des webinaires. De plus, je suis des blogs spécialisés et m’implique dans des communautés professionnelles pour être toujours à la pointe des dernières avancées.",
    "Je consacre du temps chaque semaine à la veille technologique, je suis des formations en ligne et participe à des webinaires. De plus, je suis des blogs spécialisés et m’implique dans des communautés professionnelles pour être toujours à la pointe des dernières avancées.",

    "Pour résoudre des problèmes complexes, j’adopte une approche structurée : j'analyse d’abord la situation, je définis les priorités et je procède étape par étape en impliquant les parties prenantes clés. Je teste différentes solutions et ajuste en fonction des résultats obtenus.",
    "Pour résoudre des problèmes complexes, j’adopte une approche structurée : j'analyse d’abord la situation, je définis les priorités et je procède étape par étape en impliquant les parties prenantes clés. Je teste différentes solutions et ajuste en fonction des résultats obtenus.",
    "Pour résoudre des problèmes complexes, j’adopte une approche structurée : j'analyse d’abord la situation, je définis les priorités et je procède étape par étape en impliquant les parties prenantes clés. Je teste différentes solutions et ajuste en fonction des résultats obtenus.",
    "Pour résoudre des problèmes complexes, j’adopte une approche structurée : j'analyse d’abord la situation, je définis les priorités et je procède étape par étape en impliquant les parties prenantes clés. Je teste différentes solutions et ajuste en fonction des résultats obtenus.",

    "Je commence par bien comprendre les besoins de l’entreprise et j’adapte mes solutions en conséquence. Je m’assure que chaque stratégie ou outil que je propose répond aux objectifs fixés, et je fais preuve de flexibilité pour ajuster en fonction des retours.",
    "Je commence par bien comprendre les besoins de l’entreprise et j’adapte mes solutions en conséquence. Je m’assure que chaque stratégie ou outil que je propose répond aux objectifs fixés, et je fais preuve de flexibilité pour ajuster en fonction des retours.",
    "Je commence par bien comprendre les besoins de l’entreprise et j’adapte mes solutions en conséquence. Je m’assure que chaque stratégie ou outil que je propose répond aux objectifs fixés, et je fais preuve de flexibilité pour ajuster en fonction des retours.",
    "Je commence par bien comprendre les besoins de l’entreprise et j’adapte mes solutions en conséquence. Je m’assure que chaque stratégie ou outil que je propose répond aux objectifs fixés, et je fais preuve de flexibilité pour ajuster en fonction des retours."

    "Mes voyages ont renforcé ma perspicacité en me permettant de découvrir des cultures variées, ce qui m'aide à m'adapter et à intégrer différentes perspectives dans mes projets.",
    "Mes voyages ont renforcé ma perspicacité en me permettant de découvrir des cultures variées, ce qui m'aide à m'adapter et à intégrer différentes perspectives dans mes projets.",
    "Mes voyages ont renforcé ma perspicacité en me permettant de découvrir des cultures variées, ce qui m'aide à m'adapter et à intégrer différentes perspectives dans mes projets.",
    "Mes voyages ont renforcé ma perspicacité en me permettant de découvrir des cultures variées, ce qui m'aide à m'adapter et à intégrer différentes perspectives dans mes projets.",

    "J'ai souvent été confrontée à des changements rapides dans ma vie, ce qui m'a appris à être flexible et à ajuster mes stratégies pour atteindre les objectifs fixés.",
    "J'ai souvent été confrontée à des changements rapides dans ma vie, ce qui m'a appris à être flexible et à ajuster mes stratégies pour atteindre les objectifs fixés.",
    "J'ai souvent été confrontée à des changements rapides dans ma vie, ce qui m'a appris à être flexible et à ajuster mes stratégies pour atteindre les objectifs fixés.",
    "J'ai souvent été confrontée à des changements rapides dans ma vie, ce qui m'a appris à être flexible et à ajuster mes stratégies pour atteindre les objectifs fixés.",

    "J'ai choisi l'IA car elle offre des solutions innovantes aux défis modernes et permet de transformer des idées en actions concrètes, ce qui est aligné avec mon désir de contribuer à des projets à impact.",
    "J'ai choisi l'IA car elle offre des solutions innovantes aux défis modernes et permet de transformer des idées en actions concrètes, ce qui est aligné avec mon désir de contribuer à des projets à impact.",
    "J'ai choisi l'IA car elle offre des solutions innovantes aux défis modernes et permet de transformer des idées en actions concrètes, ce qui est aligné avec mon désir de contribuer à des projets à impact.",
    "J'ai choisi l'IA car elle offre des solutions innovantes aux défis modernes et permet de transformer des idées en actions concrètes, ce qui est aligné avec mon désir de contribuer à des projets à impact.",

    "J'utilise des outils de suivi des KPIs pour m'assurer que les projets respectent les budgets alloués tout en maximisant leur efficacité.",
    "J'utilise des outils de suivi des KPIs pour m'assurer que les projets respectent les budgets alloués tout en maximisant leur efficacité.",
    "J'utilise des outils de suivi des KPIs pour m'assurer que les projets respectent les budgets alloués tout en maximisant leur efficacité.",
    "J'utilise des outils de suivi des KPIs pour m'assurer que les projets respectent les budgets alloués tout en maximisant leur efficacité.",

    "Je réalise des analyses de données approfondies pour identifier les opportunités d'amélioration, et j'utilise les KPIs pour suivre et ajuster les performances.",
    "Je réalise des analyses de données approfondies pour identifier les opportunités d'amélioration, et j'utilise les KPIs pour suivre et ajuster les performances.",
    "Je réalise des analyses de données approfondies pour identifier les opportunités d'amélioration, et j'utilise les KPIs pour suivre et ajuster les performances.",
    "Je réalise des analyses de données approfondies pour identifier les opportunités d'amélioration, et j'utilise les KPIs pour suivre et ajuster les performances.",

    "Je pense que la transformation digitale continuera d'être un levier clé pour l'innovation et l'efficacité, en particulier dans les PME cherchant à maximiser leur impact.",
    "Je pense que la transformation digitale continuera d'être un levier clé pour l'innovation et l'efficacité, en particulier dans les PME cherchant à maximiser leur impact.",
    "Je pense que la transformation digitale continuera d'être un levier clé pour l'innovation et l'efficacité, en particulier dans les PME cherchant à maximiser leur impact.",
    "Je pense que la transformation digitale continuera d'être un levier clé pour l'innovation et l'efficacité, en particulier dans les PME cherchant à maximiser leur impact.",

    "L'IA peut automatiser des tâches répétitives, améliorer l'analyse des données et optimiser la prise de décision, ce qui conduit à des gains de temps et d'efficacité.",
    "L'IA peut automatiser des tâches répétitives, améliorer l'analyse des données et optimiser la prise de décision, ce qui conduit à des gains de temps et d'efficacité.",
    "L'IA peut automatiser des tâches répétitives, améliorer l'analyse des données et optimiser la prise de décision, ce qui conduit à des gains de temps et d'efficacité.",
    "L'IA peut automatiser des tâches répétitives, améliorer l'analyse des données et optimiser la prise de décision, ce qui conduit à des gains de temps et d'efficacité.",

    "Mon double profil, mêlant compétences stratégiques et techniques, ainsi que mon expertise en IA, me permettent de proposer des solutions innovantes et alignées sur les besoins spécifiques des entreprises.",
    "Mon double profil, mêlant compétences stratégiques et techniques, ainsi que mon expertise en IA, me permettent de proposer des solutions innovantes et alignées sur les besoins spécifiques des entreprises.",
    "Mon double profil, mêlant compétences stratégiques et techniques, ainsi que mon expertise en IA, me permettent de proposer des solutions innovantes et alignées sur les besoins spécifiques des entreprises.",
    "Mon double profil, mêlant compétences stratégiques et techniques, ainsi que mon expertise en IA, me permettent de proposer des solutions innovantes et alignées sur les besoins spécifiques des entreprises.",

    "Ma première expérience de gestion a consisté à m'assurer de la compréhension des rôles de chacun et à instaurer une communication transparente pour garantir l'engagement de l'équipe.",
    "Ma première expérience de gestion a consisté à m'assurer de la compréhension des rôles de chacun et à instaurer une communication transparente pour garantir l'engagement de l'équipe.",
    "Ma première expérience de gestion a consisté à m'assurer de la compréhension des rôles de chacun et à instaurer une communication transparente pour garantir l'engagement de l'équipe.",
    "Ma première expérience de gestion a consisté à m'assurer de la compréhension des rôles de chacun et à instaurer une communication transparente pour garantir l'engagement de l'équipe.",

    "Je crois que l'IA peut transformer la manière dont nous abordons des défis majeurs, comme l'accès à l'éducation, la santé ou encore permettre de développer des projets riches de sens, en proposant des solutions efficaces et évolutives.",
    "Je crois que l'IA peut transformer la manière dont nous abordons des défis majeurs, comme l'accès à l'éducation, la santé ou encore permettre de développer des projets riches de sens, en proposant des solutions efficaces et évolutives.",
    "Je crois que l'IA peut transformer la manière dont nous abordons des défis majeurs, comme l'accès à l'éducation, la santé ou encore permettre de développer des projets riches de sens, en proposant des solutions efficaces et évolutives.",
    "Je crois que l'IA peut transformer la manière dont nous abordons des défis majeurs, comme l'accès à l'éducation, la santé ou encore permettre de développer des projets riches de sens, en proposant des solutions efficaces et évolutives.",
]

df = pd.DataFrame({'question': questions, 'answer': answers})

def read_profile_info(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def get_chatgpt_response_with_examples(profile_info, user_input, df, first_question):
    references = "\n".join([f"Q: {row['question']}\nA: {row['answer']}" for _, row in df.iterrows()])
    
    prompt = f"""
    Tu es un chatbot professionnel qui répond à des questions sur un profil professionnel en utilisant les informations du profil et des exemples de questions-réponses similaires.
    
    Voici quelques exemples de questions-réponses pour t'aider à comprendre le type de réponses attendues :
    {references}
    
    Voici les informations de mon profil :
    {profile_info}

    La question posée par l'utilisateur est : "{user_input}"

    Réponds, en maximum 5 phrases, de manière personnalisée et précise, en tenant compte des exemples ci-dessus et en adaptant la réponse pour qu'elle soit la plus pertinente possible à la question posée. Le ton doit être à la fois professionnel, convivial, et refléter l'attitude d'une jeune adulte tournée vers l'innovation. 

    Introduit chaque réponse par : "C'est une bonne question ! Merci de votre intérêt !🥳"
    """

    if first_question:
        prompt += (
            "\nPuis termine par : \"Cette réponse est générée par un LLM utilisant GPT-3.5. "
            "Mon chatbot analyse toutes les informations disponibles sur moi et mon profil pour vous fournir la réponse la plus adaptée 📊✨. "
            "Notez qu'une même question peut avoir plusieurs réponses possibles 🔄. "
            "Par exemple, si vous me demandez mes compétences, étant donné que j'en ai beaucoup 😉, la réponse pourra varier !\""
        )

    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a professional chatbot answering questions about a user's profile"},
            {"role": "user", "content": prompt}
        ]
    )
    return(response['choices'][0]['message']['content'])


st.set_page_config(page_title="Chatbot Professionnel de Ambre", page_icon="🤖", layout="wide")

st.image("assets/maphoto.png", width=150)

st.title("🤖 Mon Chatbot Professionnel")
st.markdown("<h3 style='text-align: center; color: gray;'>Développé entièrement from scratch : du code au déploiement 🚀</h3>", unsafe_allow_html=True)

st.markdown("""
Bienvenue sur mon chatbot professionnel ! 🤓 Je l'ai développé pour vous permettre d'en savoir plus sur mon parcours, de manière interactive et personnalisée. 
N'hésitez pas à poser des questions sur mes compétences, mon expérience, ma formation, ou même ma vision du monde de l’entreprise et de l’IA💡

Par exemple, vous pourriez demander : "Quelles sont tes compétences clés ?", "Comment utilises-tu l'IA dans tes projets ?", "En quoi ton profil pourrait-il apporter une valeur ajoutée à notre entreprise ?" ou encore "Quels sont tes hobbies?". 

Votre curiosité est la bienvenue, alors ne soyez pas timide et explorez tout ce que vous souhaitez savoir sur moi ! ✨💬
""")

st.markdown("### Posez moi vos questions à propos de mon profil professionnel, je me ferai un plaisir d'y répondre !")

profile_info = read_profile_info("profile_info.txt")

if "first_question" not in st.session_state:
    st.session_state.first_question = True

user_input = st.text_input("Vous : ", "")

if st.button("Me demander !"):
    if user_input:
        response = get_chatgpt_response_with_examples(profile_info, user_input, df, st.session_state.first_question)
        st.write(f"Chatbot : {response}")

        st.session_state.first_question = False

st.markdown("---")
st.markdown("Développé par Ambre Thimon. 🚀")
