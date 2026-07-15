import {
  describe,
  it,
  expect,
  beforeAll,
  afterEach,
  afterAll,
  vi,
} from "vitest";
import { mount, flushPromises } from "@vue/test-utils";
import { setupServer } from "msw/node";
import { http, HttpResponse } from "msw";
import FavoritesListView from "./FavoritesListView.vue";

vi.mock("vue-router", () => ({
  useRouter: () => ({
    push: vi.fn(),
  }),
}));

const mockApiUrl = "http://localhost:8000/api/v1/knowledge/";

let mockDatabase = [
  {
    id: 2,
    category: "Backend",
    question: "O que e FastAPI?",
    answer: "Um framework Python de alta performance.",
    favorite: true,
    created_at: "2026-07-14T12:00:00",
    updated_at: "2026-07-14T12:00:00",
  },
];

const server = setupServer(
  http.get(mockApiUrl, ({ request }) => {
    const url = new URL(request.url);
    const favoriteParam = url.searchParams.get("favorite");
    const search = url.searchParams.get("search");

    if (favoriteParam !== "true") {
      return HttpResponse.json([], { status: 400 });
    }

    let result = [...mockDatabase];
    if (search) {
      result = result.filter((item) =>
        item.question.toLowerCase().includes(search.toLowerCase()),
      );
    }

    return HttpResponse.json(result);
  }),

  http.patch(`${mockApiUrl}:id/favorite`, ({ params }) => {
    const id = Number(params.id);
    mockDatabase = mockDatabase.filter((item) => item.id !== id);
    return HttpResponse.json({ id, favorite: false });
  }),

  http.post(mockApiUrl, async ({ request }) => {
    const body = (await request.json()) as any;
    const newRecord = {
      id: 3,
      ...body,
      created_at: "2026-07-15T12:00:00",
      updated_at: "2026-07-15T12:00:00",
    };
    if (newRecord.favorite) {
      mockDatabase.push(newRecord);
    }
    return HttpResponse.json(newRecord, { status: 201 });
  }),
);

describe("FavoritesListView.vue (Integration)", () => {
  beforeAll(() => server.listen());
  afterEach(() => {
    server.resetHandlers();
    mockDatabase = [
      {
        id: 2,
        category: "Backend",
        question: "O que e FastAPI?",
        answer: "Um framework Python de alta performance.",
        favorite: true,
        created_at: "2026-07-14T12:00:00",
        updated_at: "2026-07-14T12:00:00",
      },
    ];
  });
  afterAll(() => server.close());

  it("deve carregar a tela passando favorite=true e renderizar os cards destacados da API", async () => {
    const wrapper = mount(FavoritesListView);
    expect(wrapper.find(".animate-pulse").exists()).toBe(true);

    await flushPromises();

    expect(wrapper.find(".animate-pulse").exists()).toBe(false);
    expect(wrapper.text()).toContain("O que e FastAPI?");
  });

  it("deve remover o card da lista instantaneamente ao desmarcar o favorito via clique", async () => {
    const wrapper = mount(FavoritesListView);
    await flushPromises();

    expect(wrapper.text()).toContain("O que e FastAPI?");

    const starButton = wrapper.find("button.rounded-lg");
    await starButton.trigger("click");
    await flushPromises();

    expect(wrapper.text()).not.toContain("O que e FastAPI?");
    expect(wrapper.text()).toContain(
      "Nenhum conhecimento favoritado no momento.",
    );
  });

  it("deve injetar o registro criado na lista de favoritos apenas se for marcado como favorito na modal", async () => {
    const wrapper = mount(FavoritesListView);
    await flushPromises();

    const sidebarNewButton = wrapper.find("aside button");
    await sidebarNewButton.trigger("click");

    const modalInput = wrapper.find(".fixed input");
    const modalTextareas = wrapper.findAll(".fixed textarea");
    const favoriteToggle = wrapper.find(".fixed .cursor-pointer.select-none");

    await modalInput.setValue("Database");
    await modalTextareas.at(0)!.setValue("O que e SQLModel?");
    await modalTextareas.at(1)!.setValue("Uma biblioteca ORM assincrona.");
    await favoriteToggle.trigger("click");

    const submitButton = wrapper.find(".fixed button.bg-primary");
    await submitButton.trigger("click");
    await flushPromises();

    expect(wrapper.text()).toContain("O que e SQLModel?");
  });
});
