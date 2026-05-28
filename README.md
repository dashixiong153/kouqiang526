# kouqiang526

口腔黏膜病学—“黏膜研思”智能体平台。

## 本地打开

直接打开 `index.html` 即可使用。病例图片与数字人资源位于 `assets/`。

## GitHub Pages 发布

当前项目页地址：

```text
https://dashixiong153.github.io/kouqiang526/
```

## 数据说明

当前版本使用浏览器 IndexedDB `kouqiang526_training_db` 保存学生登录信息与训练记录，同时使用 `localStorage` 保存教师看板所需的本地镜像数据。

同时支持接入 Supabase 云端数据库。教师端填写 Supabase Project URL 和 anon key 后，可将课前/课后题库、问卷、测试配置同步到云端；学生使用生成的同步链接进入后，可读取教师云端题库并把作答记录写回云端。

## Supabase 建表 SQL

在 Supabase SQL Editor 执行：

```sql
create table if not exists public.quiz_configs (
  type text primary key,
  source_mode text not null default 'builtin',
  question_count integer not null default 5,
  mode text not null default 'mixed',
  custom_questions jsonb not null default '[]'::jsonb,
  custom_survey jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now()
);

create table if not exists public.student_records (
  fid text primary key,
  student_id text,
  record_type text,
  payload jsonb not null,
  created_at timestamptz not null default now()
);

alter table public.quiz_configs enable row level security;
alter table public.student_records enable row level security;

drop policy if exists "public read quiz configs" on public.quiz_configs;
create policy "public read quiz configs"
on public.quiz_configs for select
using (true);

drop policy if exists "public write quiz configs" on public.quiz_configs;
create policy "public write quiz configs"
on public.quiz_configs for insert
with check (true);

drop policy if exists "public update quiz configs" on public.quiz_configs;
create policy "public update quiz configs"
on public.quiz_configs for update
using (true)
with check (true);

drop policy if exists "public read records" on public.student_records;
create policy "public read records"
on public.student_records for select
using (true);

drop policy if exists "public write records" on public.student_records;
create policy "public write records"
on public.student_records for insert
with check (true);

drop policy if exists "public update records" on public.student_records;
create policy "public update records"
on public.student_records for update
using (true)
with check (true);
```

说明：以上策略适合参赛演示。正式教学部署时建议改为后端服务或登录鉴权后的 RLS 策略，避免公开写入权限。
