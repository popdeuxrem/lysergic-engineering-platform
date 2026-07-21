import { render, screen } from "@testing-library/react";

import HomePage from "@/app/page";

describe("HomePage", () => {
  it("renders the operations console title", () => {
    render(<HomePage />);

    expect(
      screen.getByRole("heading", { name: /LEP Operations Console/i }),
    ).toBeInTheDocument();
  });

  it("renders the platform version", () => {
    render(<HomePage />);

    expect(
      screen.getByText(/Lysergic Engineering Platform v0.1.0/i),
    ).toBeInTheDocument();
  });
});
