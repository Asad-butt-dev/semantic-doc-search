import matplotlib.pyplot as plt
import json as js 
import pathlib as p
import numpy as np


def get_chunk_size_recall(): 
    with open(p.Path(__file__).parent/"eval/plot_scores.json","r",encoding="utf-8") as f:
      scores=js.load(f)
    xy_pair_model={"minilm-multi":[[],[]],"e5-base":[[],[]],"minilm-en":[[],[]]}
    for element in scores:
        xy_pair_model[element["model"]][0].append(element["chunk_size"])
        xy_pair_model[element["model"]][1].append(element["recall_at_1"])
    return xy_pair_model
def get_mean_categorical_metrics():
     with open(p.Path(__file__).parent/"eval/scores_categories.json","r",encoding="utf-8") as f:
          categories_scores=js.load(f)
     metrics={"Recall@1": [0.0,0.0,0.0,0.0],"Recall@5": [0.0,0.0,0.0,0.0],"Mean Reciprocal Rank": [0.0,0.0,0.0,0.0]}
     for score in categories_scores:
           for metric in ["Recall@1","Recall@5","Mean Reciprocal Rank"]:
               metrics[metric][0]+=score[list(score.keys())[0]]["specific"][metric]/10
               metrics[metric][1]+=score[list(score.keys())[0]]["broad"][metric]/10
               metrics[metric][2]+=score[list(score.keys())[0]]["formula"][metric]/10
               metrics[metric][3]+=score[list(score.keys())[0]]["conceptual"][metric]/10
     return metrics
    
def plot_model_comparison(xy_pair_model):
    plt.figure()
    plt.plot(xy_pair_model["minilm-multi"][0],xy_pair_model["minilm-multi"][1],marker="o", label="minilm-multi(128)")
    plt.plot(xy_pair_model["e5-base"][0],xy_pair_model["e5-base"][1],marker="o", label="e5-base(512)")
    plt.plot(xy_pair_model["minilm-en"][0],xy_pair_model["minilm-en"][1],marker="o", label="minilm-en(256)")
    
    plt.xlabel("Chunk size (words)")
    plt.ylabel("Recall@1")
    plt.title("Retrieval accuracy by chunk size and model")
    plt.legend()
    plt.ylim(0.65,0.9)
    plt.xticks([200,250,300,350,400,450,500,550,600,650],rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(p.Path(__file__).parent /"images"/"model_comparison.png", dpi=150,bbox_inches="tight" )

def plot_categories_comparison(metrics):
    plt.figure()
    categories=["specific (n=68)","broad (n=32)","formula (n=20)","conceptual (n=80)"]
    x=np.arange(len(categories))
    series=get_mean_categorical_metrics()
    width=0.2
    plt.bar(x-width,series["Recall@1"],width,label="Recall@1")
    plt.bar(x,series["Recall@5"],width,label="Recall@5")
    plt.bar(x+width,series["Mean Reciprocal Rank"],width,label="Mean Reciprocal Rank")
    plt.xticks(x,categories)
    
    plt.legend(loc="lower right")
    plt.ylim(0.6, 1.0)
    plt.figtext(0.5, 0.01, "Note: 4 formula questions target lecture06.pdf, which yields no text layer and is absent from the index.", ha="center", fontsize=8)
    plt.savefig(p.Path(__file__).parent /"images"/"category_comparison.png", dpi=150,bbox_inches="tight")


if __name__=="__main__":
    plot_categories_comparison(get_mean_categorical_metrics())
