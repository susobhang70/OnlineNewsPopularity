import Algorithmia

input = {
  "trainUrl":"data://susobhang70/SMAI/NewOnlineNewsPopularity.arff",
  "cv":10,
  "options":"",
  "mode":"train",
  "modelUrl":"data://.algo/temp/model.txt"
}
client = Algorithmia.client('simznouad5rhD4MLz53z6LQZc7S1')
algo = client.algo('weka/REPTree/0.1.1')
print algo.pipe(input)