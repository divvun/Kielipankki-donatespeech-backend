import summerSchedule from "../test-assets/summer-schedule.json";
export const getConfigurations = jest.fn(async () => {});

export const getConfiguration = jest.fn(async (id: string) =>
  Promise.resolve(summerSchedule)
);
