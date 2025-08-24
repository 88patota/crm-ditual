import { getNextOrderNumber } from './budgetService';
import axios from 'axios';

jest.mock('axios');
const mockedAxios = axios as unknown as jest.Mocked<typeof axios>;

describe('getNextOrderNumber', () => {
  it('should return the order number when the API call is successful', async () => {
    mockedAxios.get.mockResolvedValueOnce({ data: { order_number: '12345' } });

    const orderNumber = await getNextOrderNumber();

    expect(orderNumber).toBe('12345');
    expect(mockedAxios.get).toHaveBeenCalledWith('/budgets/next-order-number');
  });

  it('should throw an error with a user-friendly message when the API call fails', async () => {
    mockedAxios.get.mockRejectedValueOnce(new Error('Internal Server Error'));

    await expect(getNextOrderNumber()).rejects.toThrow(
      'Não foi possível obter o próximo número de pedido.'
    );
    expect(mockedAxios.get).toHaveBeenCalledWith('/budgets/next-order-number');
  });
});
