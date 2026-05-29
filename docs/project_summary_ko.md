# 프로젝트 요약: 뱀의 사지 퇴화와 SHH/ZRS 비교 분석

## 1. 탐구 질문

뱀의 사지 퇴화가 **SHH 단백질 자체의 변화** 때문인지, 아니면 SHH의 발현을 조절하는 **ZRS enhancer(조절서열)** 변화 때문인지 비교해보는 것이 이 프로젝트의 핵심이다.

## 2. 전체 연구 흐름

```text
뱀은 사지가 퇴화했다
↓
사지 발달에는 SHH가 중요하다
↓
그렇다면 뱀의 SHH 단백질 자체가 크게 변했을까?
↓
여러 척추동물의 SHH 단백질 서열을 비교했다
↓
SHH 단백질은 뱀에서도 비교적 보존되어 있었다
↓
따라서 단백질 변화보다 ZRS enhancer 같은 조절서열 변화 가능성을 분석했다
↓
뱀의 ZRS에서 ETS motif 후보들이 많이 훼손되어 있었다
```

## 3. 각 코드의 의미

### `fetch_shh_sequences.py`
NCBI accession 번호를 이용해 사람, 생쥐, 닭, 도마뱀, 뱀의 SHH protein sequence(단백질 서열)를 FASTA 형식으로 가져오는 코드다.

### `summarize_shh_sequences.py`
각 SHH 단백질의 길이를 계산한다. 이를 통해 종마다 단백질 길이가 크게 다른지 먼저 확인한다.

### `calculate_shh_similarity.py`
두 종씩 SHH 단백질 서열을 비교하여 similarity(유사도)를 계산한다. 이 단계는 “뱀의 SHH 단백질 자체가 크게 망가졌는가?”를 확인하기 위한 것이다.

### `download_zrs_alignment.py`
Ensembl REST API를 이용해 사람 기준 ZRS enhancer 영역의 여러 종 alignment(정렬)를 가져온다. ZRS는 SHH의 limb-specific expression(사지 특이적 발현)을 조절하는 enhancer로 알려져 있다.

### `scan_zrs_ets_motifs.py`
사람 ZRS에서 ETS core motif 후보인 `GGAA`, `GGAT`를 찾고, 같은 alignment 위치에서 다른 종들이 이를 보존하는지 확인한다. 보존 상태는 `conserved`, `mutated`, `gap_disrupted`로 분류했다.

### `visualize_results.py`
SHH 단백질 유사도, ZRS identity(동일성), ETS motif 상태를 그림으로 시각화한다.

## 4. 주요 결과

### SHH 단백질 비교

- Python bivittatus와 Protobothrops mucrosquamatus의 SHH 단백질 유사도는 95.31%였다.
- 사람과 두 뱀의 SHH 유사도도 각각 약 76% 수준으로 유지되었다.
- 따라서 뱀의 사지 퇴화를 단순히 “SHH 단백질이 사라졌기 때문”이라고 보기는 어렵다.

### ZRS enhancer 비교

사람 기준 ZRS와 비교했을 때 ungapped identity는 다음과 같았다.

| 비교 | identity |
|---|---:|
| human vs mouse | 89.37% |
| human vs chicken | 88.17% |
| human vs anole | 82.32% |
| human vs Pseudonaja textilis | 69.46% |

뱀에서 ZRS enhancer의 보존성이 더 낮게 나타났다.

### ETS motif 분석

Pseudonaja textilis에서는 ETS 후보 8개 중 1개만 conserved였고, 1개는 mutated, 6개는 gap_disrupted였다. 이는 뱀의 ZRS enhancer 기능 약화 가능성을 보여주는 후보 신호로 해석할 수 있다.

## 5. 결론

이 프로젝트의 결론은 다음과 같이 정리할 수 있다.

> SHH protein coding sequence(단백질 암호화 서열)는 뱀에서도 비교적 보존되어 있으므로, 뱀의 사지 퇴화는 SHH 단백질 자체의 기능 상실보다는 ZRS enhancer(조절서열)의 변화와 더 관련되었을 가능성이 있다.

단, 이 분석은 sequence-based analysis(서열 기반 분석)이므로 실제 enhancer 기능 감소를 증명하려면 reporter assay(리포터 실험), embryonic expression data(배아 발현 데이터), 더 많은 종을 포함한 comparative genomics(비교유전체학) 분석이 필요하다.
