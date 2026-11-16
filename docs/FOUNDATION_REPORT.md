# Báo cáo Foundation v0.1 — 2026-11-16

## A. Repository và nhánh

- FACT: checkout `/workspace/finance-research-intelligence` có origin HTTPS
  `github.com/nam28386/finance-research-intelligence.git`, đúng repository yêu cầu,
  không phải `vn30-dnse-live`.
- Preflight: working tree trống, chưa có commit hay `AGENTS.md` áp dụng.
  `git ls-remote --symref origin HEAD refs/heads/main` chạy thành công nhưng không
  trả refs. Default branch: UNKNOWN; chưa có remote `main` làm base cho PR.
- Nhánh làm việc: `feat/research-intelligence-foundation`. Không sửa repository
  khác, rewrite history, force-push hay merge vào main.

## B. Kiến trúc

Discovery → Source Evidence → Mechanism/Contract Extraction → Reproduction →
Validation → Knowledge Registry → Optional Project Integration.

Chỉ triển khai metadata, governance, validator và review workflow. Catalog JSON
thật để trống. Không chạy discovery, external source execution, market feeds,
ML, RAG, database, microservices hay trading. Không có scientific finding mới.

## C. Danh mục file

Tất cả là file mới, không ghi đè công việc có sẵn:

| File | Mục đích |
| --- | --- |
| `README.md` | Phạm vi và lệnh sử dụng |
| `GOALS.md` | Mục tiêu và non-goals |
| `AGENTS.md` | Hợp đồng cho agent tương lai |
| `.gitignore` | Loại cache, environment và artifacts khỏi Git |
| `docs/ARCHITECTURE.md` | Ranh giới kiến trúc và future interfaces |
| `docs/RESEARCH_GOVERNANCE.md` | Nhãn tri thức, lifecycle, evidence và human gates |
| `docs/RESEARCH_SCHEMA.md` | Field guide, semantics và giới hạn validator |
| `docs/SECURITY_BOUNDARIES.md` | Secrets, untrusted inputs và IP |
| `docs/ROADMAP.md` | Phase 01 và đề xuất Phase 02 |
| `docs/FOUNDATION_REPORT.md` | Báo cáo bàn giao này |
| `schemas/research-catalog.schema.json` | Schema version 0.1.0 |
| `research/catalog.json` | Registry rỗng, không chứa nghiên cứu giả |
| `tools/__init__.py` | Module tooling offline |
| `tools/validate_catalog.py` | Structural và semantic validation, CLI, base comparison |
| `tests/test_catalog.py` | Deterministic regression và contract tests |
| `tests/fixtures/valid_unknown.json` | Synthetic DISCOVERED, revision null/UNKNOWN |
| `tests/fixtures/valid_lifecycle.json` | Synthetic đầy đủ các promotion gates |
| `tests/fixtures/invalid_transition.json` | Synthetic transition sai phải bị từ chối |
| `.github/ISSUE_TEMPLATE/repository_research.md` | Research intake |
| `.github/ISSUE_TEMPLATE/research_experiment.md` | Falsifiable experiment proposal |
| `.github/pull_request_template.md` | Evidence, provenance và human review |
| `.github/workflows/validate.yml` | CI ít quyền, không secrets hay auto-merge |

## D. Kiểm thử thực tế

Runtime đã kiểm tra: Python 3.12.14, Git 2.52.0. Tooling và test suite chỉ dùng
Python standard library; không thêm package/dependency hoặc install script.

| Kiểm tra | Kết quả |
| --- | --- |
| `python3 -m unittest discover -s tests -v` | PASS, 23 tests, không skip/expected failure |
| `python3 -m tools.validate_catalog` | PASS, catalog thật hợp lệ |
| CLI valid_lifecycle với `--base` valid_unknown | PASS, exit 0 |
| CLI invalid_transition | PASS negative test: từ chối, exit 1 như dự kiến |
| Workflow YAML, quyền read-only, action SHA pin, shell syntax | PASS cục bộ |
| Các bước runtime/catalog và unittest của workflow | PASS cục bộ |
| GitHub-hosted Actions run, checkout action thực tế | NOT RUN |
| Research reproduction / empirical evaluation / causal identification | NOT RUN; không nằm trong Phase 01 |

YAML được parse bằng PyYAML 6.0.3 có sẵn trên máy để kiểm tra một lần; đây không
phải dependency của project hay CI. Validator không phải JSON Schema engine tổng
quát; keyword ngoài subset hỗ trợ bị từ chối. Các tham chiếu evidence là metadata
không được fetch hoặc execute. PASS không xác nhận sự thật của evidence.

Whitespace và toàn bộ bước shell của CI được kiểm tra ở bước bàn giao cuối;
kết quả cuối và commit SHA được báo trực tiếp cùng bản bàn giao. Không xem local
CI simulation là bằng chứng GitHub Actions đã chạy.

## E. Security và IP

Không thêm credentials, authentication headers, account/private market data hay
third-party implementation. URLs và SHA trong fixtures là dữ liệu synthetic được
gắn cờ rõ ràng; không được đưa vào catalog thật như nguồn đã kiểm chứng. Không có
market hypothesis được nâng thành finding vì test PASS.

Workflow dùng GitHub-hosted runner, `contents: read`, action pin theo SHA,
`persist-credentials: false`, không `pull_request_target`, secrets, deployment hay
automatic merge. Chưa cấu hình branch protection hoặc GitHub approval policy.

## F–H. Giới hạn và review

Foundation đủ điều kiện **READY FOR HUMAN REVIEW** về thay đổi cục bộ. Không đồng
nghĩa production-ready hay scientifically validated. Human review vẫn phải kiểm
tra schema/lifecycle, evidence gates và security trước khi tích hợp hoặc publish.

Remote không có base branch được quảng bá nên chưa tạo PR. Remote write permission
là NOT RUN; không suy ra quyền push từ việc đọc được Git. Dùng nhánh/commit local
để review. Khi cần PR, chủ repository cần thống nhất và khởi tạo base `main`, sau
đó đưa base vào feature branch bằng merge giữ nguyên history trước khi push/mở PR;
không tự merge vào main hoặc rebase/rewrite commit đã có. Không có PR URL để báo.

License của chính repository là UNKNOWN/chưa được chủ sở hữu lựa chọn; task này
không tự cấp license. Việc tái sử dụng third-party code trong tương lai phải được
review riêng. Validator không chứng thực reviewer, source authenticity, điều khoản
license, scientific validity hay sự tồn tại của SHA trên upstream.

## I. Phase 02 — chỉ đề xuất

Chốt phạm vi public GitHub và rubric → thu thập shortlist metadata có provenance
→ đăng ký DISCOVERED → human review chọn pilot → source review ở SHA thật → đề xuất
reproduction có rights, resource limits và falsifiers. Xem `ROADMAP.md`.
Phase 02 chưa được triển khai.
