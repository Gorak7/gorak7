import { describe, expect, it, vi } from "vitest";
import { fireEvent, render, screen } from "@testing-library/react";
import { Button, Dialog, Tabs, TextField } from "./components";

describe("your-ui primitives", () => {
  it("associates the field label with the input and emits changes", () => {
    const onChange = vi.fn();
    render(<TextField label="Display name" value="" onChange={onChange} />);
    fireEvent.change(screen.getByRole("textbox", { name: "Display name" }), { target: { value: "Gorak" } });
    expect(onChange).toHaveBeenCalledWith("Gorak");
  });
  it("supports tab selection and arrow-key navigation", () => {
    const onChange = vi.fn();
    render(<Tabs value="one" onChange={onChange} items={[{ value: "one", label: "One" }, { value: "two", label: "Two" }]} />);
    const first = screen.getByRole("tab", { name: "One" });
    first.focus();
    fireEvent.keyDown(first, { key: "ArrowRight" });
    expect(onChange).toHaveBeenCalledWith("two");
  });
  it("renders an accessible dialog when open", () => {
    render(<Dialog open title="Confirm action" onClose={vi.fn()}>Dialog content</Dialog>);
    expect(screen.getByRole("dialog", { name: "Confirm action" })).toBeInTheDocument();
  });
  it("forwards button clicks", () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Save</Button>);
    fireEvent.click(screen.getByRole("button", { name: "Save" }));
    expect(onClick).toHaveBeenCalledOnce();
  });
});