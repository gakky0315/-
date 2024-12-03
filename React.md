# インタラクティビティの追加 
## イベントへの応答

## state:コンポーネントのメモリ

### 初めてのフック
- Reactでは、useStateやその他のuseで始まる関数はフックと呼ぶ。
- フックはReactがレンダーされている間のみ利用あのうな特別な関数

### useStateの構造

### コンポーネントで複数のstate変数を使う
```java script
export default function Gallery() {
  const [index, setIndex] = useState(0);
  const [showMore, setShowMore] = useState(false);
  #いろんな処理
}
```
### stateは独立しておりプライベート
- stateは画面上の個々のコンポーネントインスタンスに対してローカル
- 言い換えると、同じコンポーネントを2回レンダーした場合、それぞれのコピーは完全に独立したstateを有することになる

### まとめ
- レンダー間で情報を「記憶」しておく必要があるコンポーネントには、state 変数を使う。
- state 変数は、useState フックを呼び出すことで宣言される。
- フックは use から始まる特殊な関数であり、state などの React 機能に「接続」できる。
- フックはインポートと似ており、無条件に呼び出す必要がある。useState などのフックの呼び出しは、コンポーネントのトップレベルか別のフックでのみ有効である。
- useState フックは、現在の state とそれを更新する関数の組み合わせを返す。
- 複数の state 変数を持つことができる。内部で React はそれらを呼び出し順を用いて対応付ける。
- state はコンポーネントにプライベートなものである。2 つの場所でレンダーすると、それぞれのコピーが独立した state を得る。

## レンダーとコミット
### 学ぶこと
- **コンポーネントは画面上に表示される前にReactによってレンダーされる必要がある** 
- Reactは変更部分だけDOMを再レンダーする


### ステップ1：レンダーのトリガ
- コンポーネントがレンダーされる理由
1. コンポーネントの初回レンダー
2. コンポーネントの**stateの更新**


#### 初回レンダー
- 初回のレンダーを取りがする必要がある
    - ターゲットとなるDOMノードに対して、createRootを呼び出し、作成されたルートのrenderメソッドをコンポーネントに対して呼び出す
```java script
const root = createRoot(document.getElementById('root'))
root.render(<Image />);
```

#### state更新後の再レンダー
- 初回レンダー後に、set関数を使ってstateを更新することで、さらなるレンダーをトリガすることができる

### ステップ2：Reactがコンポーネントをレンダー
- レンダーをトリガした後、Reactはコンポーネントを呼び出して画面に表示する内容を把握する
- レンダーとは、Reactがコンポーネントを呼び出すこと
    - 初回レンダー時：React はルート (root) コンポーネントを呼び出します。
    - 次回以降のレンダー：state の更新によってレンダーがトリガされた関数コンポーネントを、React が呼び出します。

### ステップ3：ReactがDOMへの変更をコミットする
- コンポーネントをレンダーした後、ReactはDOMを変更する
    - 初回レンダー時：ReactはappendChild() DOM APIを使用して、作成した全てのDOMノードを画面に表示
    - 再レンダー時：Reactは細心のレンダー出力に合わせてDOMを変更するため、必要最小限の操作（レンダー中に計算されたもの）を適用 
- **React はレンダー間で違いがあった場合にのみ DOM ノードを変更**

## stateはスナップショットである
### 学ぶこと
- stateはスナップショットのように振る舞う
    - スナップショット：ある特定の時点での状態 (state) の固定されたコピー

### stateのセットでレンダーがトリガされる

### レンダーは時間を切り取ってスナップショットを取る
- レンダーするとは、Reactがあなたのコンポーネント（関数）を呼び出すということ
- 関数から返されるJSXは、その時点でのUIスナップショットのようなもの

- ここでは、stateはレンダーに渡された時点でのものが更新される（）

## 一連のstateの更新をキューに入れる
- state変数をセットすることで、新しいレンダーがキューに予約される

### Reactはstate更新をまとめて処理する
- 前回やった内容は、setNumber(number + 1)を三回重ねても+1しかされない
- イベントハンドラ内の全てのコードが実行されるまで、Reactはstateの更新処理を待機

- バッチ処理：複数の操作や処理をまとめて一度実行する仕組み。Reactにおけるバッチ処理は、複数のstate更新が発生した場合に、それぞれを個別に処理するのではなく、まとめて効率的に再レンダーする動作のこと。

### 次のレンダー前に同じstateを複数回更新する
- setNumber(n => n + 1)を繰り返すことでキュー内の一つ前のstateに基づいて次のstateを計算する関数を渡すことができる
- 以下に、イベントハンドラを実行するときに、React はこれらのコードをどのように処理するかを示します。
1. setNumber(n => n + 1): n => n + 1 は関数。React はこれをキューに追加する。
2. setNumber(n => n + 1): n => n + 1 は関数。React はこれをキューに追加する。
3. setNumber(n => n + 1): n => n + 1 は関数。React はこれをキューに追加する。

|キュー内の更新処理|n|返り値|  
|-|-|-| 
|n => n + 1|0|0 + 1 = 1|  
|n => n + 1|1|1 + 1 = 2|  
|n => n + 1|2|2 + 1 = 3|

## state内のオブジェクトの更新
### ミューテーション
- オブジェクト自体の内容を書き換えること
    - ただし、React ではこれを避けるべき
- なぜミューテーションを避けるべきなのか？
    - React の state を直接変更すると、React が変更を認識できず、再レンダーが正しく行われなくなる可能性
```javascript
const [position, setPosition] = useState({ x: 0, y: 0 });
position.x = 5;
```

### stateを読み取り専用として扱う
- stateとして格納するすべてのJavaScriptオブジェクトは読み取り専門として扱う必要がある
- またはset～で更新する必要がある

### スプレッド構文を使ったオブジェクトのコピー
- オブジェクトスプレッド構文を使うことでプロパティの宣言を省略できる

- 省略前
```javascript
setPerson({
  firstName: person.firstName, 
  lastName: person.lastName,  
  email: person.email,        
  firstName: e.target.value   
});
```

- 省略後
```javascript
setPerson({
  ...person, 
  firstName: e.target.value 
});
```

### ネストされたオブジェクトの更新
-
```javascript
const [person, setPerson] = useState({
  name: 'Niki de Saint Phalle',
  artwork: {
    title: 'Blue Nana',
    city: 'Hamburg',
    image: 'https://i.imgur.com/Sd1AgUOm.jpg',
  }
});
```
- 以下の二つのオブジェクトスプレッド構文で更新できる
1. ステップごとに書く場合
```javascript
const nextArtwork = { ...person.artwork, city: 'New Delhi' }; 
const nextPerson = { ...person, artwork: nextArtwork };      
setPerson(nextPerson);                            
```

2. まとめて書く場合
```javascript
setPerson({
  ...person, 
  artwork: { 
    ...person.artwork, 
    city: 'New Delhi'  
  }
});
```

### Immerで簡潔な更新ロジックを書く
- Immer を使うと、ネストされたオブジェクトをスプレッド構文で手動コピーする必要がなくなり、次のように簡潔に書けます：
```javascript
const [person, setPerson] = useState({
  name: 'John Doe',
  artwork: {
    title: 'Masterpiece',
    city: 'Paris',
    image: 'https://example.com/image.jpg'
  }
});

// city を更新
setPerson({
  ...person, // person をコピー
  artwork: {
    ...person.artwork, // artwork をコピー
    city: 'Lagos' // city を更新
  }
});
```

```javascript
import { useImmer } from 'use-immer';

function App() {
  const [person, updatePerson] = useImmer({
    name: 'John Doe',
    artwork: {
      title: 'Masterpiece',
      city: 'Paris',
      image: 'https://example.com/image.jpg'
    }
  });

  function handleCityChange() {
    updatePerson(draft => {
      draft.artwork.city = 'Lagos'; // 直接変更しているように書ける
    });
  }

  return (
    <button onClick={handleCityChange}>
      Update City
    </button>
  );
}
```

## state内の配列の更新

### 配列を書き換えずに更新する
- 配列をイミュータブルとして扱う理由
    - Reactが変更を検知できない
    - コードの予測可能性を保つ

### 配列に要素を追加
- オブジェクトスプレッド構文を使う
- 変更前
```javascript
<button onClick={() => {
        artists.push({
          id: nextId++,
          name: name,
        });
      }}>Add</button>
```
- 変更後
```javascript
<button onClick={() => {
        setArtists([
          ...artists,
          { id: nextId++, name: name }
        ]);
      }}>Add</button>
```

### 配列から要素を削除
- 配列から要素を削除する方法はフィルタリングして取り除いた新しい配列を作ること
    - filterメソッドを使用

### 配列の変換
- 配列の一部またはすべての要素を変更したい場合
    - map()を使用して新しい配列を作成
```javascript
function handleClick() {
    const nextShapes = shapes.map(shape => {
      if (shape.type === 'square') {
        return shape;
      } else {
        return {
          ...shape,
          y: shape.y + 50,
        };
      }
    });
    setShapes(nextShapes);
  }
```

### 配列内の要素の置換
- 配列内の一部の要素だけを置き換えたい場合
    - mapを使って新しい配列を作成する

```javascript
function handleIncrementClick(index) {
    const nextCounters = counters.map((c, i) => {
      if (i === index) {
        return c + 1;
      } else {
        return c;
      }
    });
    setCounters(nextCounters);
  }
```

### 配列の挿入
- 先頭でも終端でもない特定の位置に要素を挿入したいとき
    - ...配列スプレッド構文×slice()メソッド

```javascript
 function handleClick() {
    const insertAt = 1; // Could be any index
    const nextArtists = [
      // Items before the insertion point:
      ...artists.slice(0, insertAt),
      // New item:
      { id: nextId++, name: name },
      // Items after the insertion point:
      ...artists.slice(insertAt)
    ];
    setArtists(nextArtists);
    setName('');
  }
```
- slice(0, insertAt)
    - 配列 artists の中から、挿入位置 insertAt の前までの要素を取得
- artists.slice(insertAt)
    - 配列 artists の中から、挿入位置 insertAt 以降の要素を取得
- nextId++ はユニークな ID を生成する仕組み

### 配列へのその他の変更

### 配列内のオブジェクトを更新する

### Immer を使って簡潔な更新ロジックを書く























# stateの管理


















# メモ
- 以下の二つは同じなので注意
```javascript
<button onClick={() => {
  setNumber(number + 5);
  setTimeout(() => {
    alert(number);
  }, 0);
}}>+5</button>

```
```javascript
function handleClick() {
  setNumber(number + 5);
  alert(number);
}

<button onClick={handleClick}>+5</button>
```












