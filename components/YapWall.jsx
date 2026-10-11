'use client';

import { useEffect, useState } from 'react';
import { Flame, MessageCircle, Send } from 'lucide-react';

const STORAGE_KEY = 'kerry-yaps-community-feed-v1';

const CATEGORIES = [
  'All',
  'Relationships',
  'Mindset',
  'Tech & AI',
  'Culture',
  'Money & Ambition',
];

const INITIAL_YAPS = [
  {
    id: 'yap-1',
    author: 'Anonymous',
    location: 'Nairobi',
    category: 'Relationships',
    text: 'The biggest friendship red flag is feeling like you have to shrink yourself just to keep the peace.',
    flames: 38,
    mics: 24,
    replies: [
      {
        id: 'reply-101',
        author: '@thequiettake',
        text: 'And when you finally speak at full volume, they call you difficult.',
      },
    ],
  },
  {
    id: 'yap-2',
    author: '@thequiettake',
    location: '',
    category: 'Mindset',
    text: 'Maybe the problem isn’t that we overthink. Maybe we keep ignoring what we already know.',
    flames: 52,
    mics: 19,
    replies: [],
  },
  {
    id: 'yap-3',
    author: 'Anonymous',
    location: 'Nairobi',
    category: 'Money & Ambition',
    text: 'We need an episode on black tax, not just the money part, but the silent emotional guilt of having boundaries.',
    flames: 64,
    mics: 41,
    replies: [],
  },
];

function createId(prefix) {
  return `${prefix}-${globalThis.crypto?.randomUUID?.() ?? `${Date.now()}-${Math.random().toString(36).slice(2)}`}`;
}

export default function YapWall() {
  const [yaps, setYaps] = useState(INITIAL_YAPS);
  const [activeCategory, setActiveCategory] = useState('All');
  const [take, setTake] = useState('');
  const [handle, setHandle] = useState('');
  const [selectedTopic, setSelectedTopic] = useState('Mindset');
  const [openReplyId, setOpenReplyId] = useState(null);
  const [replyTexts, setReplyTexts] = useState({});
  const [storageReady, setStorageReady] = useState(false);

  useEffect(() => {
    try {
      const savedYaps = window.localStorage.getItem(STORAGE_KEY);
      if (savedYaps) setYaps(JSON.parse(savedYaps));
    } catch {
      // Keep the in-memory feed usable if browser storage is unavailable.
    }
    setStorageReady(true);
  }, []);

  useEffect(() => {
    if (!storageReady) return;
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(yaps));
    } catch {
      // Local persistence is optional; interactions still work for this session.
    }
  }, [yaps, storageReady]);

  const handlePostYap = (event) => {
    event.preventDefault();
    const text = take.trim();
    if (!text) return;

    const newYap = {
      id: createId('yap'),
      author: handle.trim() || 'Anonymous',
      location: '',
      category: selectedTopic,
      text,
      flames: 0,
      mics: 0,
      replies: [],
    };

    setYaps((current) => [newYap, ...current]);
    setTake('');
    setHandle('');
  };

  const handleReaction = (id, type) => {
    setYaps((current) => current.map((yap) => (
      yap.id === id ? { ...yap, [type]: yap[type] + 1 } : yap
    )));
  };

  const handleAddReply = (event, yapId) => {
    event.preventDefault();
    const text = (replyTexts[yapId] || '').trim();
    if (!text) return;

    setYaps((current) => current.map((yap) => (
      yap.id === yapId
        ? {
            ...yap,
            replies: [
              ...yap.replies,
              { id: createId('reply'), author: handle.trim() || 'Listener', text },
            ],
          }
        : yap
    )));
    setReplyTexts((current) => ({ ...current, [yapId]: '' }));
  };

  const filteredYaps = activeCategory === 'All'
    ? yaps
    : yaps.filter((yap) => yap.category === activeCategory);

  return (
    <div className="min-h-screen bg-[#1C1413] px-4 py-12 text-[#F3E7DA] selection:bg-[#D4AF37]/30">
      <div className="mx-auto max-w-2xl space-y-8">
        <header className="space-y-2 text-center">
          <span className="text-xs font-medium uppercase tracking-widest text-[#D4AF37]">
            Community Board
          </span>
          <h1 className="font-serif text-4xl text-[#F7EFE5] md:text-5xl">
            The Yap Wall
          </h1>
          <p className="text-sm text-[#A89F91]">
            Drop your takes, lessons, and unpopular opinions. Unfiltered &amp; unapologetic.
          </p>
        </header>

        <form
          onSubmit={handlePostYap}
          className="space-y-3 rounded-2xl border border-[#3E2723] bg-[#241917] p-4 shadow-xl"
        >
          <div className="flex flex-col gap-2 sm:flex-row">
            <label htmlFor="yap-category" className="sr-only">Yap category</label>
            <select
              id="yap-category"
              value={selectedTopic}
              onChange={(event) => setSelectedTopic(event.target.value)}
              className="w-full rounded-lg border border-[#3E2723] bg-[#1C1413] px-2.5 py-1.5 text-xs text-[#D4AF37] focus:border-[#D4AF37] focus:outline-none sm:w-auto"
            >
              {CATEGORIES.filter((category) => category !== 'All').map((category) => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
            <label htmlFor="yap-handle" className="sr-only">Your handle (optional)</label>
            <input
              id="yap-handle"
              type="text"
              maxLength={40}
              placeholder="@handle or Anonymous"
              value={handle}
              onChange={(event) => setHandle(event.target.value)}
              className="min-w-0 w-full flex-1 rounded-lg border border-[#3E2723] bg-[#1C1413] px-3 py-1.5 text-xs text-[#F7EFE5] focus:border-[#D4AF37] focus:outline-none"
            />
          </div>

          <label htmlFor="yap-take" className="sr-only">Put your thought on the table</label>
          <textarea
            id="yap-take"
            rows={3}
            maxLength={280}
            placeholder="Put your thought on the table..."
            value={take}
            onChange={(event) => setTake(event.target.value)}
            className="w-full resize-none rounded-xl border border-[#3E2723] bg-[#1C1413] p-3 text-sm text-[#F7EFE5] placeholder:text-[#6E6359] focus:border-[#D4AF37] focus:outline-none"
          />

          <div className="flex items-center justify-between pt-1">
            <span aria-live="polite" className="text-[11px] text-[#7A6F64]">
              {280 - take.length} chars left · Saved on this device only
            </span>
            <button
              type="submit"
              disabled={!take.trim()}
              className="inline-flex items-center gap-1.5 rounded-xl bg-[#D4AF37] px-4 py-2 text-xs font-medium text-[#1C1413] transition hover:bg-[#C29D26] disabled:cursor-not-allowed disabled:opacity-40"
            >
              Post Yap <Send size={13} aria-hidden="true" />
            </button>
          </div>
        </form>

        <nav aria-label="Filter yaps by category" className="flex flex-wrap gap-2 pb-1">
          {CATEGORIES.map((category) => (
            <button
              key={category}
              type="button"
              onClick={() => setActiveCategory(category)}
              aria-pressed={activeCategory === category}
              className={`whitespace-nowrap rounded-full px-3.5 py-1.5 text-xs transition ${
                activeCategory === category
                  ? 'bg-[#D4AF37] font-semibold text-[#1C1413]'
                  : 'border border-[#3E2723] bg-[#241917] text-[#A89F91] hover:text-[#F3E7DA]'
              }`}
            >
              {category}
            </button>
          ))}
        </nav>

        <div className="space-y-4">
          {filteredYaps.length === 0 && (
            <p className="rounded-2xl border border-[#3E2723] bg-[#241917] p-6 text-center text-sm text-[#A89F91]">
              No yaps in this category yet. Be the first to start the conversation.
            </p>
          )}
          {filteredYaps.map((yap) => (
            <article
              key={yap.id}
              className="space-y-3 rounded-2xl border border-[#3E2723] bg-[#241917] p-5"
            >
              <div className="flex items-center justify-between gap-3 text-xs">
                <span className="font-medium text-[#F7EFE5]">
                  {yap.author}{' '}
                  {yap.location && <span className="text-[#7A6F64]">· {yap.location}</span>}
                </span>
                <span className="rounded-full border border-[#3E2723] bg-[#1C1413] px-2.5 py-0.5 text-[10px] text-[#D4AF37]">
                  {yap.category}
                </span>
              </div>

              <p className="whitespace-pre-wrap break-words text-sm leading-relaxed text-[#F3E7DA]">
                “{yap.text}”
              </p>

              <div className="flex items-center gap-4 border-t border-[#34221F] pt-3 text-xs text-[#A89F91]">
                <button
                  type="button"
                  onClick={() => handleReaction(yap.id, 'flames')}
                  aria-label={`React with fire, ${yap.flames} reactions`}
                  className="flex min-h-8 items-center gap-1 transition hover:text-[#D4AF37]"
                >
                  <Flame size={14} className="text-[#E07A5F]" aria-hidden="true" />
                  <span>{yap.flames}</span>
                </button>
                <button
                  type="button"
                  onClick={() => handleReaction(yap.id, 'mics')}
                  aria-label={`React with microphone, ${yap.mics} reactions`}
                  className="flex min-h-8 items-center gap-1 transition hover:text-[#D4AF37]"
                >
                  <span aria-hidden="true">🎙️</span>
                  <span>{yap.mics}</span>
                </button>
                <button
                  type="button"
                  onClick={() => setOpenReplyId(openReplyId === yap.id ? null : yap.id)}
                  aria-expanded={openReplyId === yap.id}
                  className="ml-auto flex min-h-8 items-center gap-1 transition hover:text-[#F7EFE5]"
                >
                  <MessageCircle size={14} aria-hidden="true" />
                  <span>{yap.replies.length} yap back</span>
                </button>
              </div>

              {yap.replies.length > 0 && (
                <div className="mt-2 space-y-2 rounded-xl border border-[#34221F] bg-[#1C1413]/70 p-3">
                  {yap.replies.map((reply) => (
                    <div key={reply.id} className="space-y-0.5 text-xs">
                      <span className="font-medium text-[#D4AF37]">{reply.author}:</span>{' '}
                      <span className="text-[#EADCCF]">{reply.text}</span>
                    </div>
                  ))}
                </div>
              )}

              {openReplyId === yap.id && (
                <form onSubmit={(event) => handleAddReply(event, yap.id)} className="flex gap-2 pt-2">
                  <label htmlFor={`reply-${yap.id}`} className="sr-only">Reply to {yap.author}</label>
                  <input
                    id={`reply-${yap.id}`}
                    type="text"
                    maxLength={280}
                    placeholder="Yap back..."
                    value={replyTexts[yap.id] || ''}
                    onChange={(event) => setReplyTexts((current) => ({ ...current, [yap.id]: event.target.value }))}
                    className="min-w-0 flex-1 rounded-xl border border-[#3E2723] bg-[#1C1413] px-3 py-2 text-xs text-[#F7EFE5] focus:border-[#D4AF37] focus:outline-none"
                  />
                  <button
                    type="submit"
                    disabled={!(replyTexts[yap.id] || '').trim()}
                    className="rounded-xl bg-[#D4AF37] px-3 py-1.5 text-xs font-medium text-[#1C1413] disabled:cursor-not-allowed disabled:opacity-40"
                  >
                    Reply
                  </button>
                </form>
              )}
            </article>
          ))}
        </div>

        <p className="pt-6 text-center text-[11px] text-[#6E6359]">
          Selected community takes get featured and discussed on Kerry Yaps Podcast. · Moderated for safety.
        </p>
      </div>
    </div>
  );
}
